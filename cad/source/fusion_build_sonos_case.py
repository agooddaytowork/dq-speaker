import adsk.core
import adsk.fusion
import math
import json


MM = 0.1  # Fusion API internal unit is cm.


def pt(x, y, z):
    return adsk.core.Point3D.create(x * MM, y * MM, z * MM)


def vec(x, y, z):
    return adsk.core.Vector3D.create(x, y, z)


def make_box(tb, sx, sy, sz, cx, cy, cz):
    obb = adsk.core.OrientedBoundingBox3D.create(
        pt(cx, cy, cz), vec(1, 0, 0), vec(0, 1, 0),
        sx * MM, sy * MM, sz * MM
    )
    return tb.createBox(obb)


def make_cyl(tb, x1, y1, z1, x2, y2, z2, radius):
    return tb.createCylinderOrCone(
        pt(x1, y1, z1), radius * MM,
        pt(x2, y2, z2), radius * MM
    )


def make_rotated_box_y(tb, sx, sy, sz, cx, cy, cz, angle_deg):
    body = make_box(tb, sx, sy, sz, cx, cy, cz)
    transform = adsk.core.Matrix3D.create()
    transform.setToRotation(math.radians(angle_deg), vec(0, 1, 0), pt(cx, cy, cz))
    if not tb.transform(body, transform):
        raise RuntimeError('Cannot rotate logo stroke')
    return body


def boolean(tb, target, tool, operation, label):
    ok = tb.booleanOperation(target, tool, operation)
    if not ok:
        raise RuntimeError('Boolean failed: ' + label)
    return target


def unite(tb, target, tool, label):
    return boolean(tb, target, tool, adsk.fusion.BooleanTypes.UnionBooleanType, label)


def cut(tb, target, tool, label):
    return boolean(tb, target, tool, adsk.fusion.BooleanTypes.DifferenceBooleanType, label)


def intersect(tb, target, tool, label):
    return boolean(tb, target, tool, adsk.fusion.BooleanTypes.IntersectionBooleanType, label)


def rounded_prism(tb, width, depth, radius, z0, z1):
    height = z1 - z0
    zc = (z0 + z1) / 2
    body = make_box(tb, width - 2 * radius, depth, height, 0, 0, zc)
    unite(tb, body, make_box(tb, width, depth - 2 * radius, height, 0, 0, zc), 'rounded-cross')
    for x in (-width / 2 + radius, width / 2 - radius):
        for y in (-depth / 2 + radius, depth / 2 - radius):
            unite(tb, body, make_cyl(tb, x, y, z0, x, y, z1, radius), 'rounded-corner')
    return body


def rounded_ring(tb, outer_w, outer_d, outer_r, wall, z0, z1):
    body = rounded_prism(tb, outer_w, outer_d, outer_r, z0, z1)
    inner = rounded_prism(
        tb, outer_w - 2 * wall, outer_d - 2 * wall,
        outer_r - wall, z0 - 0.5, z1 + 0.5
    )
    return cut(tb, body, inner, 'rounded-ring-hollow')


def capsule_cutter_x(tb, center_x, center_y, center_z, total_length, width, through_depth):
    straight = total_length - width
    half = straight / 2
    body = make_box(tb, straight, through_depth, width, center_x, center_y, center_z)
    for x in (center_x - half, center_x + half):
        cyl = make_cyl(
            tb, x, center_y - through_depth / 2, center_z,
            x, center_y + through_depth / 2, center_z, width / 2
        )
        unite(tb, body, cyl, 'capsule-x-end')
    return body


def capsule_cutter_y(tb, center_x, center_y, center_z, total_length, width, through_depth):
    straight = total_length - width
    half = straight / 2
    body = make_box(tb, through_depth, straight, width, center_x, center_y, center_z)
    for y in (center_y - half, center_y + half):
        cyl = make_cyl(
            tb, center_x - through_depth / 2, y, center_z,
            center_x + through_depth / 2, y, center_z, width / 2
        )
        unite(tb, body, cyl, 'capsule-y-end')
    return body


def capsule_cutter_corner(tb, corner_x, corner_y, angle_deg, center_z,
                          radius, total_length, width, through_depth):
    angle = math.radians(angle_deg)
    center_x = corner_x + radius * math.cos(angle)
    center_y = corner_y + radius * math.sin(angle)
    body = capsule_cutter_x(
        tb, center_x, center_y, center_z,
        total_length, width, through_depth
    )
    # Rotate the through direction onto the corner radius. The capsule's long
    # axis then follows the local tangent of the rounded sleeve wall.
    transform = adsk.core.Matrix3D.create()
    transform.setToRotation(
        math.radians(angle_deg - 90.0), vec(0, 0, 1),
        pt(center_x, center_y, center_z)
    )
    if not tb.transform(body, transform):
        raise RuntimeError('Cannot orient rounded-corner vent cutter')
    return body


def add_component(parent_component, name):
    occurrence = parent_component.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occurrence.component.name = name
    return occurrence, occurrence.component


def add_body(component, temp_body, name, appearance=None):
    base_feature = component.features.baseFeatures.add()
    base_feature.name = 'BF_' + name
    if not base_feature.startEdit():
        raise RuntimeError('Cannot edit base feature for ' + name)
    body = component.bRepBodies.add(temp_body, base_feature)
    if not body:
        raise RuntimeError('Cannot persist body ' + name)
    if not base_feature.finishEdit():
        raise RuntimeError('Cannot finish base feature for ' + name)
    body = component.bRepBodies.item(component.bRepBodies.count - 1)
    body.name = name
    if appearance:
        body.appearance = appearance
    return body


def _edge_signature_mm(edge):
    if not edge.startVertex or not edge.endVertex:
        return None
    if not adsk.core.Line3D.cast(edge.geometry):
        return None
    a = edge.startVertex.geometry
    b = edge.endVertex.geometry
    av = (a.x * 10, a.y * 10, a.z * 10)
    bv = (b.x * 10, b.y * 10, b.z * 10)
    delta = tuple(abs(bv[i] - av[i]) for i in range(3))
    axis = 'xyz'[delta.index(max(delta))]
    midpoint = tuple((av[i] + bv[i]) / 2 for i in range(3))
    return axis, midpoint, edge.length * 10


def find_linear_edges(body, axis, targets, coord_tol=0.15, length_tol=0.2):
    found = []
    for edge in body.edges:
        signature = _edge_signature_mm(edge)
        if not signature or signature[0] != axis:
            continue
        _, midpoint, length = signature
        for target_x, target_y, target_z, target_length in targets:
            target = (target_x, target_y, target_z)
            if all(abs(midpoint[i] - target[i]) <= coord_tol for i in range(3)) and abs(length - target_length) <= length_tol:
                found.append(edge)
                break
    return found


def add_frame_fillet_feature(component, body, half):
    if half == 'rear':
        main_targets = [
            (x, -40.25, z, 7.5)
            for x in (-56.5, 56.5) for z in (17.75, 202.25)
        ]
        # Receiver overlap changes the two outer root edges slightly, so select
        # the four inner and four outer roots by their actual post-join topology.
        root_targets = [
            (x, -36.5, z, 8.5)
            for x in (-52.25, 52.25) for z in (23.0, 197.0)
        ] + [
            (x, -36.0, z, 8.613)
            for x in (-53.694, 53.694) for z in (13.0, 207.0)
        ]
    elif half == 'front':
        main_targets = [
            (x, 40.0, z, 8.0)
            for x in (-56.5, 56.5) for z in (17.75, 202.25)
        ]
        root_targets = [
            (x, 36.0, z, 4.5)
            for x in (-60.25, 60.25) for z in (14.0, 22.0, 198.0, 206.0)
        ]
    else:
        raise RuntimeError('Unknown frame half for fillet: ' + half)

    main_edges = find_linear_edges(body, 'y', main_targets)
    root_edges = find_linear_edges(body, 'x', root_targets)
    if len(main_edges) != 4 or len(root_edges) != 8:
        raise RuntimeError(
            'Fillet edge audit failed for %s: main=%d root=%d' %
            (half, len(main_edges), len(root_edges))
        )

    fillets = component.features.filletFeatures
    fillet_input = fillets.createInput()
    main_collection = adsk.core.ObjectCollection.create()
    root_collection = adsk.core.ObjectCollection.create()
    for edge in main_edges:
        main_collection.add(edge)
    for edge in root_edges:
        root_collection.add(edge)
    fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
        main_collection, adsk.core.ValueInput.createByString('3 mm'), False
    )
    fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
        root_collection, adsk.core.ValueInput.createByString('2 mm'), False
    )
    feature = fillets.add(fillet_input)
    if not feature:
        raise RuntimeError('Fusion FilletFeature failed for ' + half)
    feature.name = half.upper() + '_STRUCTURAL_FILLET_R3_R2'
    return feature


def add_frame_branch_root_fillet_feature(component, body, half):
    """Round every remaining load-bearing rectangular branch-to-rail root.

    Functional edges at screw holes, insert seats, cap datum faces, and pin
    tips are intentionally excluded so the already validated fit is retained.
    """
    if half == 'rear':
        targets = [
            (x, -40.0, z, 8.0)
            for x in (-56.5, 56.5)
            for z in (100.25, 108.25, 161.25, 169.25)
        ]
        targets += [
            (-56.5, -40.0, z, 8.0)
            for z in (26.25, 33.25, 68.75, 75.75)
        ]
        targets += [
            (x, -40.0, 17.75, 8.0)
            for x in (-1.5, 4.5)
        ]
    elif half == 'front':
        targets = [
            (x, 40.0, z, 8.0)
            for x in (-56.5, 56.5)
            for z in (54.25, 62.25, 100.25, 108.25, 161.25, 169.25)
        ]
    else:
        raise RuntimeError('Unknown frame half for branch fillet: ' + half)

    edges = find_linear_edges(body, 'y', targets, coord_tol=0.2, length_tol=0.25)
    if len(edges) != len(targets):
        raise RuntimeError(
            'Branch-root edge audit failed for %s: found=%d expected=%d' %
            (half, len(edges), len(targets))
        )

    collection = adsk.core.ObjectCollection.create()
    for edge in edges:
        collection.add(edge)
    fillet_input = component.features.filletFeatures.createInput()
    fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
        collection, adsk.core.ValueInput.createByString('1.5 mm'), False
    )
    feature = component.features.filletFeatures.add(fillet_input)
    if not feature:
        raise RuntimeError('Fusion branch-root FilletFeature failed for ' + half)
    feature.name = half.upper() + '_ALL_STRUCTURAL_BRANCH_ROOTS_R1_5'
    return feature


def add_param(design, name, expression, unit, comment):
    return design.userParameters.add(
        name, adsk.core.ValueInput.createByString(expression), unit, comment
    )


def make_appearance(design, name, rgba, roughness):
    appearance = design.appearances.add(name)
    appearance.color = adsk.core.Color.create(rgba[0], rgba[1], rgba[2], rgba[3])
    appearance.roughness = roughness
    return appearance


def source_to_product_transform():
    # Right-handed +90-degree rotation about X, then center the V6 envelope.
    # newX = oldX - 48.5; newY = -oldZ - 47; newZ = oldY + 165.25.
    matrix = adsk.core.Matrix3D.create()
    matrix.setCell(0, 0, 1.0)
    matrix.setCell(0, 1, 0.0)
    matrix.setCell(0, 2, 0.0)
    matrix.setCell(0, 3, -48.5 * MM)
    matrix.setCell(1, 0, 0.0)
    matrix.setCell(1, 1, 0.0)
    matrix.setCell(1, 2, -1.0)
    matrix.setCell(1, 3, -47.0 * MM)
    matrix.setCell(2, 0, 0.0)
    matrix.setCell(2, 1, 1.0)
    matrix.setCell(2, 2, 0.0)
    matrix.setCell(2, 3, 165.25 * MM)
    matrix.setCell(3, 0, 0.0)
    matrix.setCell(3, 1, 0.0)
    matrix.setCell(3, 2, 0.0)
    matrix.setCell(3, 3, 1.0)
    return matrix


def find_reference_bodies(root):
    rear_name = 'Body1_REAR_MOUNTING_ROUNDED_PRODUCTION_V6:1'
    front_name = 'Fit_Test_FRONT_4MM_PINS_ROUNDED_PRODUCTION_V6:1'
    rear_body = None
    front_body = None
    for occurrence in root.allOccurrences:
        if occurrence.name == rear_name and occurrence.bRepBodies.count:
            rear_body = occurrence.bRepBodies.item(0)
        if occurrence.name == front_name and occurrence.bRepBodies.count:
            front_body = occurrence.bRepBodies.item(0)
    if not rear_body or not front_body:
        raise RuntimeError('The two V6 reference occurrences were not found in the active source document')
    return rear_body, front_body


def build_rear_frame(tb):
    y0, y1 = -44.0, -36.0
    z_min, z_max = 11.75, 208.25
    body = make_box(tb, 6, y1 - y0, z_max - z_min, -59.5, (y0 + y1) / 2, 110)
    unite(tb, body, make_box(tb, 6, 8, z_max - z_min, 59.5, -40, 110), 'rear-right-rail')
    unite(tb, body, make_box(tb, 125, 8, 6, 0, -40, z_min + 3), 'rear-bottom-rail')
    unite(tb, body, make_box(tb, 125, 8, 6, 0, -40, z_max - 3), 'rear-top-rail')

    # Four audited Ø3 mounting holes and their structural bosses.
    for x in (-48.5, 48.5):
        for z in (165.25, 104.25):
            side_x = -59.5 if x < 0 else 59.5
            arm_length = abs(side_x - x) + 8.0
            unite(tb, body, make_box(tb, arm_length, 8, 8, (side_x + x) / 2, -40, z), 'rear-local-m3-arm')
            unite(tb, body, make_cyl(tb, x, -44, z, x, -10, z, 3.0), 'rear-6mm-m3-boss')
            cut(tb, body, make_cyl(tb, x, -45, z, x, -9, z, 1.5), 'rear-m3-hole')

    # Secondary audited Ø2 mounting holes retained from V6.
    # Continuous service spine for the two central M2 mounting bosses. Extend
    # it into the bottom rail so these mounting features cannot remain as a
    # disconnected lump inside the exported frame body.
    unite(tb, body, make_box(tb, 6, 8, 65, 1.5, -40, 49.0), 'rear-connected-service-spine')
    for x in (-45.5, 1.5):
        for z in (72.25, 29.75):
            if x < -20:
                unite(tb, body, make_box(tb, 18, 8, 7, -54.0, -40, z), 'rear-local-m2-arm')
            unite(tb, body, make_cyl(tb, x, -44, z, x, -10, z, 3.0), 'rear-m2-boss')
            cut(tb, body, make_cyl(tb, x, -45, z, x, -9, z, 1.0), 'rear-m2-hole')

    # Four compact M3 insert receivers integrated into the rear frame.
    # The mating tie posts belong entirely to the front frame, so the rear half
    # does not grow a second arm into the speaker volume.
    for side in (-1, 1):
        x_center = side * 53.0
        for z in (18.0, 202.0):
            unite(tb, body, make_box(tb, 10, 11, 10, x_center, -31, z), 'rear-integrated-insert-receiver')
            if side > 0:
                pilot = make_cyl(tb, 47.5, -31, z, 58.5, -31, z, 2.1)
            else:
                pilot = make_cyl(tb, -58.5, -31, z, -47.5, -31, z, 2.1)
            cut(tb, body, pilot, 'rear-integrated-insert-pilot')

    # Bottom M3 insert bosses, two on rear half.
    for x in (-45.0, 45.0):
        unite(tb, body, make_cyl(tb, x, -35, 8, x, -35, 22, 4.5), 'rear-bottom-boss')
        cut(tb, body, make_cyl(tb, x, -35, 7.5, x, -35, 17, 2.1), 'rear-bottom-insert-pilot')

    # Two M3 top-cap insert bosses belonging to the rear half.
    for x in (-45.0, 45.0):
        unite(tb, body, make_cyl(tb, x, -35, 198, x, -35, 212, 4.5), 'rear-top-m3-boss')
        cut(tb, body, make_cyl(tb, x, -35, 204.5, x, -35, 212.5, 2.1), 'rear-top-m3-insert-pilot')
    return body


def build_front_frame(tb):
    y0, y1 = 36.0, 44.0
    z_min, z_max = 11.75, 208.25
    body = make_box(tb, 6, y1 - y0, z_max - z_min, -59.5, 40, 110)
    unite(tb, body, make_box(tb, 6, 8, z_max - z_min, 59.5, 40, 110), 'front-right-rail')
    unite(tb, body, make_box(tb, 125, 8, 6, 0, 40, z_min + 3), 'front-bottom-rail')
    unite(tb, body, make_box(tb, 125, 8, 6, 0, 40, z_max - 3), 'front-top-rail')

    pin_positions = [
        (-48.5, 165.25), (48.5, 165.25),
        (-48.5, 104.25), (48.5, 104.25),
        (-47.0, 58.25), (47.0, 58.25)
    ]
    for x, z in pin_positions:
        side_x = -59.5 if x < 0 else 59.5
        arm_length = abs(side_x - x) + 8.0
        unite(tb, body, make_box(tb, arm_length, 8, 8, (side_x + x) / 2, 40, z), 'front-local-pin-arm')
        unite(tb, body, make_cyl(tb, x, 32, z, x, 44, z, 4.0), 'front-pin-base')
        unite(tb, body, make_cyl(tb, x, 10.5, z, x, 44, z, 2.1), 'front-4p2mm-pin')

    # Four continuous tie posts, owned by this half only, run beside the
    # acoustic keepout.  Their rear terminal pads overlap the compact insert
    # receivers in the rear frame and accept side-access M3x16 screws.
    for side in (-1, 1):
        x_center = side * 61.0
        for z in (18.0, 202.0):
            unite(tb, body, make_box(tb, 6, 67, 8, x_center, 2.5, z), 'front-single-tie-post')
            unite(tb, body, make_box(tb, 6, 9, 10, x_center, -31, z), 'front-tie-post-terminal')
            if side > 0:
                clearance = make_cyl(tb, 57.5, -31, z, 64.5, -31, z, 1.7)
                counterbore = make_cyl(tb, 60.5, -31, z, 64.5, -31, z, 3.1)
            else:
                clearance = make_cyl(tb, -64.5, -31, z, -57.5, -31, z, 1.7)
                counterbore = make_cyl(tb, -64.5, -31, z, -60.5, -31, z, 3.1)
            cut(tb, body, clearance, 'front-tie-post-m3-clearance')
            cut(tb, body, counterbore, 'front-tie-post-head-counterbore')

    # Bottom M3 insert bosses, two on front half.
    for x in (-45.0, 45.0):
        unite(tb, body, make_cyl(tb, x, 35, 8, x, 35, 22, 4.5), 'front-bottom-boss')
        cut(tb, body, make_cyl(tb, x, 35, 7.5, x, 35, 17, 2.1), 'front-bottom-insert-pilot')

    # Two M3 top-cap insert bosses belonging to the front half.
    for x in (-45.0, 45.0):
        unite(tb, body, make_cyl(tb, x, 35, 198, x, 35, 212, 4.5), 'front-top-m3-boss')
        cut(tb, body, make_cyl(tb, x, 35, 204.5, x, 35, 212.5, 2.1), 'front-top-m3-insert-pilot')
    return body


def build_sleeve(tb):
    body = rounded_ring(tb, 133, 133, 27, 2.0, 5.5, 214.5)
    slot_length = 5.4
    slot_width = 2.2
    pitch_x = 10.0
    pitch_z = 6.0
    row_count = 30
    z_start = 23.0
    flat_limit = 36.5
    corner_center = 39.5
    corner_slot_radius = 27.0
    cuts = 0

    for row in range(row_count):
        z = z_start + row * pitch_z
        offset = 5.0 if row % 2 else 0.0
        candidates = [i * pitch_x + offset for i in range(-5, 6)]
        for c in candidates:
            if abs(c) > flat_limit:
                continue
            # Front and back flat faces. Rear keeps a 27 mm service spine.
            cutter = capsule_cutter_x(tb, c, 66.5, z, slot_length, slot_width, 7.0)
            cut(tb, body, cutter, 'sleeve-front-slot')
            cuts += 1
            if abs(c) >= 13.5:
                cutter = capsule_cutter_x(tb, c, -66.5, z, slot_length, slot_width, 7.0)
                cut(tb, body, cutter, 'sleeve-rear-slot')
                cuts += 1

            # Left and right flat faces; slot tangent follows Y.
            cutter = capsule_cutter_y(tb, 66.5, c, z, slot_length, slot_width, 7.0)
            cut(tb, body, cutter, 'sleeve-right-slot')
            cuts += 1
            cutter = capsule_cutter_y(tb, -66.5, c, z, slot_length, slot_width, 7.0)
            cut(tb, body, cutter, 'sleeve-left-slot')
            cuts += 1

        # Wrap the perforation field across all four R27 corner surfaces.
        # Alternating 4/5-slot rows continue the stagger without a straight
        # vertical seam at the flat-to-curve transition.
        local_angles = (18.0, 36.0, 54.0, 72.0) if row % 2 == 0 else (9.0, 27.0, 45.0, 63.0, 81.0)
        corner_defs = (
            ( corner_center,  corner_center,   0.0),
            (-corner_center,  corner_center,  90.0),
            (-corner_center, -corner_center, 180.0),
            ( corner_center, -corner_center, 270.0),
        )
        for corner_x, corner_y, quadrant_start in corner_defs:
            for local_angle in local_angles:
                cutter = capsule_cutter_corner(
                    tb, corner_x, corner_y, quadrant_start + local_angle, z,
                    corner_slot_radius, slot_length, slot_width, 7.0
                )
                cut(tb, body, cutter, 'sleeve-rounded-corner-slot')
                cuts += 1
        if row % 4 == 0:
            adsk.doEvents()
    return body, cuts


def build_top_cap(tb):
    body = rounded_prism(tb, 135, 135, 28, 212, 224)
    groove = rounded_ring(tb, 133.5, 133.5, 27.25, 2.5, 211.5, 215.0)
    cut(tb, body, groove, 'top-cap-sleeve-groove')

    # Port axes derived from V6: 16 mm pitch, intentionally Ø13 power and Ø11 USB-C.
    cut(tb, body, make_cyl(tb, 17.95, -9.0, 202, 17.95, -9.0, 225, 5.5), 'usb-c-11mm')
    cut(tb, body, make_cyl(tb, 33.95, -9.0, 202, 33.95, -9.0, 225, 6.5), 'power-13mm')

    # Four serviceable M3x16 screws enter from the top, like the bottom cap.
    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            cut(tb, body, make_cyl(tb, x, y, 211, x, y, 225, 1.7), 'top-m3-clearance')
            cut(tb, body, make_cyl(tb, x, y, 218.8, x, y, 224, 3.2), 'top-m3-head-recess')
            cut(tb, body, make_cyl(tb, x, y, 222.3, x, y, 224.5, 4.6), 'top-screw-plug-pocket')
            pry_y = y + (4.5 if y > 0 else -4.5)
            cut(tb, body, make_cyl(tb, x, pry_y, 222.0, x, pry_y, 224.5, 0.9), 'top-screw-plug-pry-notch')

    # Raised rounded DQ monogram on the front wall (+Y), 0.8 mm visible relief.
    # Circular strokes echo the case corner radius and avoid the previous
    # industrial block-letter look.
    logo_y0, logo_y1 = 67.3, 68.3
    zc = 218.0

    # Model X is mirrored when the +Y front wall is viewed from outside.
    # Place D at +X and put its spine on +X so the user reads D on the left.
    d_curve = make_cyl(tb, 6.0, logo_y0, zc, 6.0, logo_y1, zc, 4.2)
    cut(tb, d_curve, make_cyl(tb, 6.0, logo_y0 - 0.1, zc, 6.0, logo_y1 + 0.1, zc, 2.4), 'rounded-logo-D-counter')
    # Retain only the model -X semicircle; outside-view mirroring makes it the
    # right-hand curve of the uppercase D.
    intersect(tb, d_curve, make_box(tb, 4.4, 1.4, 9.0, 3.9, 67.8, zc), 'rounded-logo-D-half-curve')
    unite(tb, d_curve, make_box(tb, 1.6, logo_y1 - logo_y0, 8.4, 10.0, (logo_y0 + logo_y1) / 2, zc), 'rounded-logo-D-spine')
    unite(tb, d_curve, make_box(tb, 4.2, logo_y1 - logo_y0, 1.8, 8.0, (logo_y0 + logo_y1) / 2, zc + 3.3), 'rounded-logo-D-top')
    unite(tb, d_curve, make_box(tb, 4.2, logo_y1 - logo_y0, 1.8, 8.0, (logo_y0 + logo_y1) / 2, zc - 3.3), 'rounded-logo-D-bottom')
    unite(tb, body, d_curve, 'rounded-logo-D')

    q_outer = make_cyl(tb, -5.5, logo_y0, zc, -5.5, logo_y1, zc, 4.2)
    cut(tb, q_outer, make_cyl(tb, -5.5, logo_y0 - 0.1, zc, -5.5, logo_y1 + 0.1, zc, 2.4), 'rounded-logo-Q-counter')
    unite(tb, q_outer, make_rotated_box_y(tb, 4.0, logo_y1 - logo_y0, 1.25, -8.2, (logo_y0 + logo_y1) / 2, 215.3, -45), 'rounded-logo-Q-tail')
    unite(tb, body, q_outer, 'rounded-logo-Q')
    return body


def build_top_screw_plugs(tb):
    plugs = []
    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            plug = make_cyl(tb, x, y, 222.4, x, y, 224.0, 4.45)
            pry_y = y + (4.45 if y > 0 else -4.45)
            cut(tb, plug, make_cyl(tb, x, pry_y, 222.2, x, pry_y, 224.2, 0.8), 'screw-plug-pry-scallop')
            plugs.append(plug)
    return plugs


def build_bottom_cap(tb):
    body = rounded_prism(tb, 135, 135, 28, 0, 8)
    groove = rounded_ring(tb, 133.5, 133.5, 27.25, 2.5, 5.0, 8.5)
    cut(tb, body, groove, 'bottom-cap-sleeve-groove')

    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            cut(tb, body, make_cyl(tb, x, y, -1, x, y, 18, 1.7), 'bottom-m3-clearance')
            cut(tb, body, make_cyl(tb, x, y, -0.5, x, y, 3.0, 3.2), 'bottom-m3-head-recess')

    # Four shallow rubber-foot locating pockets.
    for x in (-50.0, 50.0):
        for y in (-50.0, 50.0):
            cut(tb, body, make_cyl(tb, x, y, -0.2, x, y, 0.8, 5.0), 'rubber-foot-pocket')
    return body


def add_hardware_check(tb, component, metal_app, insert_app, rubber_app):
    # M3 frame-joint screw envelopes at the rear terminal of each front-owned
    # tie post, accessible from the two outer side faces.
    index = 1
    for side in (-1, 1):
        for z in (18.0, 202.0):
            if side > 0:
                shaft = make_cyl(tb, 48, -31, z, 64, -31, z, 1.5)
                unite(tb, shaft, make_cyl(tb, 61, -31, z, 64, -31, z, 3.0), 'joint-screw-head')
                insert = make_cyl(tb, 51.0, -31, z, 56.7, -31, z, 2.3)
            else:
                shaft = make_cyl(tb, -64, -31, z, -48, -31, z, 1.5)
                unite(tb, shaft, make_cyl(tb, -64, -31, z, -61, -31, z, 3.0), 'joint-screw-head')
                insert = make_cyl(tb, -56.7, -31, z, -51.0, -31, z, 2.3)
            add_body(component, shaft, 'M3x16_FRAME_%02d' % index, metal_app)
            add_body(component, insert, 'M3_INSERT_FRAME_%02d' % index, insert_app)
            index += 1

    # M3 bottom screw envelopes.
    index = 1
    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            shaft = make_cyl(tb, x, y, 0, x, y, 16, 1.5)
            unite(tb, shaft, make_cyl(tb, x, y, -3, x, y, 0, 3.0), 'bottom-screw-head')
            add_body(component, shaft, 'M3x16_BOTTOM_%02d' % index, metal_app)
            insert = make_cyl(tb, x, y, 10, x, y, 15.7, 2.3)
            add_body(component, insert, 'M3_INSERT_BOTTOM_%02d' % index, insert_app)
            index += 1

    # Four M3x16 top screw envelopes, hidden only by the removable cover.
    index = 1
    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            shaft = make_cyl(tb, x, y, 206.2, x, y, 222.2, 1.5)
            unite(tb, shaft, make_cyl(tb, x, y, 219.2, x, y, 222.2, 3.0), 'top-m3-head')
            add_body(component, shaft, 'M3x16_TOP_%02d' % index, metal_app)
            insert = make_cyl(tb, x, y, 205.0, x, y, 210.7, 2.3)
            add_body(component, insert, 'M3_INSERT_TOP_%02d' % index, insert_app)
            index += 1

    # Four rubber feet below the bottom cap.
    for index, (x, y) in enumerate(((-50, -50), (-50, 50), (50, -50), (50, 50)), start=1):
        foot = make_cyl(tb, x, y, -2.5, x, y, 0, 5.0)
        add_body(component, foot, 'RUBBER_FOOT_%02d' % index, rubber_app)


def run(_context: str):
    app = adsk.core.Application.get()
    source_doc = app.activeDocument
    source_design = adsk.fusion.Design.cast(app.activeProduct)
    if not source_design:
        raise RuntimeError('The active document is not a Fusion design')
    if source_doc.name != 'TEST-BACK2-SONOS-ONE-SL-ROUNDED-V6':
        raise RuntimeError('Expected active V6 source, got: ' + source_doc.name)
    if not source_doc.isSaved or not source_doc.dataFile:
        raise RuntimeError('The V6 source must already have a cloud data location')

    source_folder = source_doc.dataFile.parentFolder
    tb = adsk.fusion.TemporaryBRepManager.get()
    rear_source, front_source = find_reference_bodies(source_design.rootComponent)
    rear_ref = tb.copy(rear_source)
    front_ref = tb.copy(front_source)
    transform = source_to_product_transform()
    if not tb.transform(rear_ref, transform):
        raise RuntimeError('Cannot transform rear reference')
    if not tb.transform(front_ref, transform):
        raise RuntimeError('Cannot transform front reference')

    new_doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    root = design.rootComponent

    parameters = [
        ('caseWidth', '135 mm', 'mm', 'Overall case width'),
        ('caseDepth', '135 mm', 'mm', 'Overall case depth'),
        ('caseHeight', '224 mm', 'mm', 'Overall case height with thicker top cap'),
        ('cornerRadius', '28 mm', 'mm', 'Outer rounded-square radius'),
        ('sleeveWall', '2.0 mm', 'mm', 'Grey PETG sleeve wall'),
        ('sleeveOuterSize', '133 mm', 'mm', 'Sleeve outside width and depth'),
        ('sleeveHeight', '209 mm', 'mm', 'Printed sleeve height including groove engagement'),
        ('topCapVisibleHeight', '12 mm', 'mm', 'Visible height of structural orange top cap'),
        ('bottomCapVisibleHeight', '8 mm', 'mm', 'Visible height of orange bottom cap'),
        ('topScrewPlugThickness', '1.6 mm', 'mm', 'Flush removable PETG screw plugs'),
        ('topScrewPlugDia', '8.9 mm', 'mm', 'Diameter of each local M3 screw plug'),
        ('grooveDepth', '3 mm', 'mm', 'Sleeve groove depth in each cap'),
        ('sleeveEngagement', '2.5 mm', 'mm', 'Sleeve engagement into each groove'),
        ('grooveRadialClearance', '0.25 mm', 'mm', 'Per-side groove clearance'),
        ('ventSlotLength', '5.4 mm', 'mm', 'Capsule slot total length'),
        ('ventSlotWidth', '2.2 mm', 'mm', 'Capsule slot width'),
        ('ventPitchX', '10 mm', 'mm', 'Dense capsule slot pitch in row'),
        ('ventPitchZ', '6 mm', 'mm', 'Dense capsule row pitch'),
        ('cornerVentRadius', '27 mm', 'mm', 'Vent cutter center radius on rounded sleeve corners'),
        ('cornerVentAngularPitch', '18 deg', 'deg', 'Nominal tangent-slot pitch around each corner'),
        ('powerCutoutDia', '13 mm', 'mm', 'Power button top cutout'),
        ('usbCutoutDia', '11 mm', 'mm', 'USB-C top cutout'),
        ('portCenterPitch', '16 mm', 'mm', 'V6-derived port center pitch'),
        ('m3ScrewLength', '16 mm', 'mm', 'Available M3 screw length'),
        ('m2ScrewLength', '10 mm', 'mm', 'Available M2 screw length'),
        ('frameJointScrewCount', '4', '', 'M3 screws joining frame halves at side rails'),
        ('framePeripheralJointX', '64 mm', 'mm', 'Outer side face of flush-access frame joints'),
        ('frameJointPlaneY', '-31 mm', 'mm', 'Rear terminal plane of front-owned tie posts'),
        ('frameTiePostX', '61 mm', 'mm', 'Tie-post centerline beside acoustic keepout'),
        ('frameMainCornerFillet', '3 mm', 'mm', 'Internal radius at main rail junctions'),
        ('frameJointRootFillet', '2 mm', 'mm', 'Root radius at tie posts and insert receivers'),
        ('frameBranchRootFillet', '1.5 mm', 'mm', 'Root radius at all remaining structural 90-degree frame branches'),
        ('frontMountingColumnDia', '4.2 mm', 'mm', 'Diameter of the six front mounting columns'),
        ('frontRedEdgeColumnShiftZ', '-5 mm', 'mm', 'Shift of the opposite front column pair toward the marked red edge'),
        ('rearMountingBossDia', '6 mm', 'mm', 'Outer diameter of the four rear mounting-hole columns'),
        ('acousticKeepoutWidth', '105 mm', 'mm', 'Central acoustic keepout width'),
        ('acousticKeepoutDepth', '70 mm', 'mm', 'Central acoustic keepout depth')
    ]
    for name, expression, unit, comment in parameters:
        add_param(design, name, expression, unit, comment)

    grey = make_appearance(design, 'PETG Bambu Lab - Grey', (92, 98, 104, 255), 0.62)
    orange = make_appearance(design, 'PETG Bambu Lab - Orange', (242, 103, 24, 255), 0.55)
    frame_color = make_appearance(design, 'PETG Bambu Lab - Frame Any Color', (35, 40, 46, 255), 0.58)
    reference_color = make_appearance(design, 'Reference V6', (60, 130, 210, 255), 0.45)
    metal = make_appearance(design, 'Fastener Steel', (145, 150, 158, 255), 0.25)
    brass = make_appearance(design, 'Heat-set Insert Brass', (190, 135, 40, 255), 0.30)
    rubber = make_appearance(design, 'Rubber Feet', (20, 20, 22, 255), 0.85)

    ref_occ, ref_group = add_component(root, '00_REFERENCE_DO_NOT_EDIT')
    rear_ref_occ, rear_ref_comp = add_component(ref_group, 'REF_REAR_V6')
    front_ref_occ, front_ref_comp = add_component(ref_group, 'REF_FRONT_V6')
    add_body(rear_ref_comp, rear_ref, 'REF_REAR_V6_MASTER', reference_color)
    add_body(front_ref_comp, front_ref, 'REF_FRONT_V6_MASTER', reference_color)
    ref_occ.isLightBulbOn = False

    frame_occ, frame_assembly = add_component(root, '01_FRAME_ASSEMBLY')
    rear_occ, rear_component = add_component(frame_assembly, '01A_REAR_FRAME')
    front_occ, front_component = add_component(frame_assembly, '01B_FRONT_FRAME')
    rear_frame = build_rear_frame(tb)
    rear_body = add_body(rear_component, rear_frame, 'REAR_FRAME_INSERT_RECEIVER_V5', frame_color)
    add_frame_fillet_feature(rear_component, rear_body, 'rear')
    add_frame_branch_root_fillet_feature(rear_component, rear_component.bRepBodies.item(0), 'rear')
    front_frame = build_front_frame(tb)
    front_body = add_body(front_component, front_frame, 'FRONT_FRAME_SINGLE_TIE_POST_V5', frame_color)
    add_frame_fillet_feature(front_component, front_body, 'front')
    add_frame_branch_root_fillet_feature(front_component, front_component.bRepBodies.item(0), 'front')
    adsk.doEvents()

    sleeve_occ, sleeve_component = add_component(root, '02_OUTER_SLEEVE_GREY')
    sleeve, slot_count = build_sleeve(tb)
    add_body(sleeve_component, sleeve, 'OUTER_SLEEVE_PERFORATED', grey)
    adsk.doEvents()

    top_occ, top_component = add_component(root, '03_TOP_CAP_ORANGE')
    add_body(top_component, build_top_cap(tb), 'TOP_CAP_M3_SERVICE_DQ_V6', orange)

    cover_occ, cover_component = add_component(root, '03B_TOP_SCREW_PLUGS_ORANGE')
    for index, plug in enumerate(build_top_screw_plugs(tb), start=1):
        add_body(cover_component, plug, 'TOP_SCREW_PLUG_%02d' % index, orange)

    bottom_occ, bottom_component = add_component(root, '04_BOTTOM_CAP_ORANGE')
    add_body(bottom_component, build_bottom_cap(tb), 'BOTTOM_CAP_M3_SERVICE', orange)

    hardware_occ, hardware_component = add_component(root, '90_HARDWARE_CHECK')
    add_hardware_check(tb, hardware_component, metal, brass, rubber)
    hardware_occ.isLightBulbOn = False

    root.isOriginFolderLightBulbOn = False
    app.activeViewport.fit()
    adsk.doEvents()

    saved = new_doc.saveAs(
        'SONOS_CASE_CONCEPT_V1', source_folder,
        'Six-part PETG speaker enclosure concept derived from V6 fit-test references',
        'speaker case; PETG; M3x16; M2x10'
    )
    if not saved:
        raise RuntimeError('Fusion saveAs failed')

    report = {
        'document': new_doc.name,
        'saved': new_doc.isSaved,
        'designType': int(design.designType),
        'slotCuts': slot_count,
        'rootOccurrences': [root.occurrences.item(i).component.name for i in range(root.occurrences.count)],
        'printParts': [
            '01A_REAR_FRAME', '01B_FRONT_FRAME', '02_OUTER_SLEEVE_GREY',
            '03_TOP_CAP_ORANGE', '03B_TOP_SCREW_PLUGS_ORANGE (4 pcs)', '04_BOTTOM_CAP_ORANGE'
        ],
        'hardwareDefault': {'M3x16': 12, 'M2x10': 0, 'rubberFeet': 4}
    }
    print(json.dumps(report, indent=2))
