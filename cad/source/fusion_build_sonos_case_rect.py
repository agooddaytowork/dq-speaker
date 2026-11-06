import adsk.core
import adsk.fusion
import math

import fusion_build_sonos_case as base


SLEEVE_WIDTH = 133.0
SLEEVE_DEPTH = 97.0
SLEEVE_RADIUS = 7.0
CAP_WIDTH = 135.0
CAP_DEPTH = 99.0
CAP_RADIUS = 8.0
TOP_POCKET_DEPTH = 8.0
TOP_SKIN = 4.0
TOP_POCKET_TO_GROOVE_WALL = 2.5
TOP_SCREW_ISLAND_RADIUS = 9.0
HANDLE_BASE_Z0 = 224.0
HANDLE_BASE_Z1 = 229.0
HANDLE_GRIP_Z = 260.0
HANDLE_SCREW_SEAT_Z = 223.8
RUBBER_FOOT_POSITIONS = ((-55.0, -28.0), (-55.0, 28.0), (55.0, -28.0), (55.0, 28.0))


def build_rect_sleeve(tb):
    body = base.rounded_ring(
        tb, SLEEVE_WIDTH, SLEEVE_DEPTH, SLEEVE_RADIUS,
        2.0, 5.5, 214.5
    )
    slot_length = 5.4
    slot_width = 2.2
    pitch = 10.0
    row_count = 30
    z_start = 23.0
    front_y = SLEEVE_DEPTH / 2
    side_x = SLEEVE_WIDTH / 2
    flat_limit_x = 56.5
    flat_limit_y = 37.5
    corner_x = side_x - SLEEVE_RADIUS
    corner_y = front_y - SLEEVE_RADIUS
    cuts = 0

    for row in range(row_count):
        z = z_start + row * 6.0
        offset = 5.0 if row % 2 else 0.0

        for i in range(-6, 7):
            x = i * pitch + offset
            if abs(x) > flat_limit_x:
                continue
            cutter = base.capsule_cutter_x(
                tb, x, front_y, z, slot_length, slot_width, 7.0
            )
            base.cut(tb, body, cutter, 'rect-sleeve-front-slot')
            cuts += 1
            if abs(x) >= 13.5:
                cutter = base.capsule_cutter_x(
                    tb, x, -front_y, z, slot_length, slot_width, 7.0
                )
                base.cut(tb, body, cutter, 'rect-sleeve-rear-slot')
                cuts += 1

        for i in range(-4, 5):
            y = i * pitch + offset
            if abs(y) > flat_limit_y:
                continue
            cutter = base.capsule_cutter_y(
                tb, side_x, y, z, slot_length, slot_width, 7.0
            )
            base.cut(tb, body, cutter, 'rect-sleeve-right-slot')
            cuts += 1
            cutter = base.capsule_cutter_y(
                tb, -side_x, y, z, slot_length, slot_width, 7.0
            )
            base.cut(tb, body, cutter, 'rect-sleeve-left-slot')
            cuts += 1

        # The tighter R7 corner has room for one tangent capsule per row.
        # Alternating its angular position avoids a straight vertical seam.
        local_angle = 35.0 if row % 2 == 0 else 55.0
        corner_defs = (
            (corner_x, corner_y, 0.0),
            (-corner_x, corner_y, 90.0),
            (-corner_x, -corner_y, 180.0),
            (corner_x, -corner_y, 270.0),
        )
        for cx, cy, quadrant_start in corner_defs:
            cutter = base.capsule_cutter_corner(
                tb, cx, cy, quadrant_start + local_angle, z,
                SLEEVE_RADIUS, slot_length, slot_width, 7.0
            )
            base.cut(tb, body, cutter, 'rect-sleeve-corner-slot')
            cuts += 1

        if row % 4 == 0:
            adsk.doEvents()
    return body, cuts


def build_rect_top_cap(tb):
    body = base.rounded_prism(tb, CAP_WIDTH, CAP_DEPTH, CAP_RADIUS, 212, 224)
    groove = base.rounded_ring(tb, 133.5, 97.5, 7.25, 2.5, 211.5, 215.0)
    base.cut(tb, body, groove, 'rect-top-cap-sleeve-groove')

    # Open an 8 mm service pocket from the inside so the USB-C and power
    # retaining nuts can be reached.  The pocket stops at Z=220, leaving a
    # 4 mm top skin.  Its perimeter stays 2.5 mm inside the sleeve-groove
    # inner edge, and four R9 islands retain the M3 head-seat structure.
    pocket_width = 123.5
    pocket_depth = 87.5
    pocket_radius = 2.25
    pocket = base.rounded_prism(tb, pocket_width, pocket_depth, pocket_radius, 211.5, 220.0)
    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            island = base.make_cyl(
                tb, x, y, 211.0, x, y, 220.5, TOP_SCREW_ISLAND_RADIUS
            )
            base.cut(tb, pocket, island, 'rect-top-pocket-m3-island')
    base.cut(tb, body, pocket, 'rect-top-inner-service-pocket-8mm')

    base.cut(tb, body, base.make_cyl(tb, 17.95, -9.0, 202, 17.95, -9.0, 225, 5.5), 'usb-c-11mm')
    base.cut(tb, body, base.make_cyl(tb, 33.95, -9.0, 202, 33.95, -9.0, 225, 6.5), 'power-13mm')

    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            base.cut(tb, body, base.make_cyl(tb, x, y, 211, x, y, 225, 1.7), 'top-m3-clearance')
            base.cut(tb, body, base.make_cyl(tb, x, y, 218.8, x, y, 224, 3.2), 'top-m3-head-recess')
            base.cut(tb, body, base.make_cyl(tb, x, y, 222.3, x, y, 224.5, 4.6), 'top-screw-plug-pocket')
            pry_y = y + (4.5 if y > 0 else -4.5)
            base.cut(tb, body, base.make_cyl(tb, x, pry_y, 222.0, x, pry_y, 224.5, 0.9), 'top-screw-plug-pry-notch')

    logo_y0, logo_y1 = 49.3, 50.3
    logo_mid_y = (logo_y0 + logo_y1) / 2
    zc = 218.0
    d_curve = base.make_cyl(tb, 6.0, logo_y0, zc, 6.0, logo_y1, zc, 4.2)
    base.cut(tb, d_curve, base.make_cyl(tb, 6.0, logo_y0 - 0.1, zc, 6.0, logo_y1 + 0.1, zc, 2.4), 'rounded-logo-D-counter')
    base.intersect(tb, d_curve, base.make_box(tb, 4.4, 1.4, 9.0, 3.9, logo_mid_y, zc), 'rounded-logo-D-half-curve')
    base.unite(tb, d_curve, base.make_box(tb, 1.6, logo_y1 - logo_y0, 8.4, 10.0, logo_mid_y, zc), 'rounded-logo-D-spine')
    base.unite(tb, d_curve, base.make_box(tb, 4.2, logo_y1 - logo_y0, 1.8, 8.0, logo_mid_y, zc + 3.3), 'rounded-logo-D-top')
    base.unite(tb, d_curve, base.make_box(tb, 4.2, logo_y1 - logo_y0, 1.8, 8.0, logo_mid_y, zc - 3.3), 'rounded-logo-D-bottom')
    base.unite(tb, body, d_curve, 'rounded-logo-D')

    q_outer = base.make_cyl(tb, -5.5, logo_y0, zc, -5.5, logo_y1, zc, 4.2)
    base.cut(tb, q_outer, base.make_cyl(tb, -5.5, logo_y0 - 0.1, zc, -5.5, logo_y1 + 0.1, zc, 2.4), 'rounded-logo-Q-counter')
    base.unite(tb, q_outer, base.make_rotated_box_y(tb, 4.0, logo_y1 - logo_y0, 1.25, -8.2, logo_mid_y, 215.3, -45), 'rounded-logo-Q-tail')
    base.unite(tb, body, q_outer, 'rounded-logo-Q')
    return body


def build_rect_top_handle(tb):
    # Two shallow V bases reuse the four cap/frame fastener centers and
    # converge onto a centered fore/aft grip.  This leaves the USB-C and power
    # openings in a clear bay with no rail running beside either cutout.
    arm_width = 8.0
    rail_zc = (HANDLE_BASE_Z0 + HANDLE_BASE_Z1) / 2

    def make_v_arm(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        length = math.sqrt(dx * dx + dy * dy)
        arm = base.make_box(
            tb, length, arm_width, HANDLE_BASE_Z1 - HANDLE_BASE_Z0,
            (x0 + x1) / 2, (y0 + y1) / 2, rail_zc
        )
        transform = adsk.core.Matrix3D.create()
        transform.setToRotation(
            math.atan2(dy, dx), base.vec(0, 0, 1),
            base.pt((x0 + x1) / 2, (y0 + y1) / 2, rail_zc)
        )
        if not tb.transform(arm, transform):
            raise RuntimeError('Cannot orient V-handle base arm')
        return arm

    support_y = 25.0
    arm_defs = (
        (-45.0, -35.0, 0.0, -support_y),
        (45.0, -35.0, 0.0, -support_y),
        (-45.0, 35.0, 0.0, support_y),
        (45.0, 35.0, 0.0, support_y),
    )
    body = make_v_arm(*arm_defs[0])
    for arm_def in arm_defs[1:]:
        base.unite(tb, body, make_v_arm(*arm_def), 'handle-v-base-arm')

    # Ø12 mounting pads make the rail ends rounded and provide bearing area.
    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            base.unite(
                tb, body,
                base.make_cyl(
                    tb, x, y, HANDLE_BASE_Z0,
                    x, y, HANDLE_BASE_Z1, 6.0
                ),
                'handle-rounded-mount-pad'
            )

    # Two centered supports and a fore/aft grip form the raised handle.
    for y in (-support_y, support_y):
        base.unite(
            tb, body,
            base.make_cyl(
                tb, 0.0, y, 227.0,
                0.0, y, HANDLE_GRIP_Z, 7.0
            ),
            'handle-vertical-support'
        )
    base.unite(
        tb, body,
        base.make_cyl(
            tb, 0.0, -35.0, HANDLE_GRIP_Z,
            0.0, 35.0, HANDLE_GRIP_Z, 7.0
        ),
        'handle-ergonomic-grip'
    )
    for y in (-support_y, support_y, -35.0, 35.0):
        base.unite(
            tb, body,
            tb.createSphere(base.pt(0.0, y, HANDLE_GRIP_Z), 7.0 * base.MM),
            'handle-rounded-grip-elbow'
        )

    # Ø8.9 locators enter the existing Ø9.2 screw-plug pockets.  The recessed
    # M3 head seats at Z=223.8; an M3x20 tip reaches Z=203.8 and therefore
    # crosses the full Z=204.5..212 insert length without needing M3x30.
    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            base.unite(
                tb, body,
                base.make_cyl(tb, x, y, 222.4, x, y, 224.1, 4.45),
                'handle-upper-plug-pocket-locator'
            )
            base.cut(
                tb, body,
                base.make_cyl(tb, x, y, 218.5, x, y, 268.0, 1.7),
                'handle-m3-clearance'
            )
            base.cut(
                tb, body,
                base.make_cyl(
                    tb, x, y, HANDLE_SCREW_SEAT_Z,
                    x, y, 268.0, 3.15
                ),
                'handle-recessed-m3-head-access'
            )
    return body


def _add_handle_fillet(component, edges, radius_expression, name, tangent_chain=False):
    if not edges:
        raise RuntimeError('No edges selected for ' + name)
    collection = adsk.core.ObjectCollection.create()
    for edge in edges:
        collection.add(edge)
    fillet_input = component.features.filletFeatures.createInput()
    fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
        collection, adsk.core.ValueInput.createByString(radius_expression), tangent_chain
    )
    feature = component.features.filletFeatures.add(fillet_input)
    if not feature:
        raise RuntimeError('Handle FilletFeature failed: ' + name)
    feature.name = name
    return feature


def add_handle_all_edge_fillet_features(component, body):
    features = []

    # First round all four support roots as one native feature.
    root_edges = []
    for edge in body.edges:
        if not adsk.core.Arc3D.cast(edge.geometry):
            continue
        bb = edge.boundingBox
        x0, x1 = bb.minPoint.x * 10, bb.maxPoint.x * 10
        y0, y1 = bb.minPoint.y * 10, bb.maxPoint.y * 10
        z0, z1 = bb.minPoint.z * 10, bb.maxPoint.z * 10
        y_center = (y0 + y1) / 2
        if (
            abs(z0 - HANDLE_BASE_Z1) < 0.1 and
            abs(z1 - HANDLE_BASE_Z1) < 0.1 and
            max(abs(x0), abs(x1)) < 8.0 and
            15.0 < abs(y_center) < 35.0
        ):
            root_edges.append(edge)
    if len(root_edges) != 4:
        raise RuntimeError('Expected four support-root arcs, found %d' % len(root_edges))
    features.append(_add_handle_fillet(
        component, root_edges, '2 mm', 'HANDLE_SUPPORT_ROOTS_NATIVE_FILLET_R2'
    ))

    # Round the complete exposed perimeter of all four V arms and mounting
    # pads.  Tangent-chain propagation is required after the root fillet has
    # split the arm ends into short analytic/NURBS edge segments.
    body = component.bRepBodies.item(0)
    exterior_edges = []
    for edge in body.edges:
        if not (adsk.core.Line3D.cast(edge.geometry) or adsk.core.Arc3D.cast(edge.geometry)):
            continue
        bb = edge.boundingBox
        x0, x1 = bb.minPoint.x * 10, bb.maxPoint.x * 10
        y0, y1 = bb.minPoint.y * 10, bb.maxPoint.y * 10
        z0, z1 = bb.minPoint.z * 10, bb.maxPoint.z * 10
        horizontal = abs(z0 - z1) < 0.05 and (
            abs(z0 - HANDLE_BASE_Z0) < 0.1 or abs(z0 - HANDLE_BASE_Z1) < 0.1
        )
        vertical = (
            abs(z0 - HANDLE_BASE_Z0) < 0.1 and
            abs(z1 - HANDLE_BASE_Z1) < 0.1 and
            edge.length * 10 > 4.9
        )
        y_center = (y0 + y1) / 2
        near_support = max(abs(x0), abs(x1)) < 10.0 and 15.0 < abs(y_center) < 35.0
        if (horizontal or vertical) and not near_support:
            exterior_edges.append(edge)
    if len(exterior_edges) != 32:
        raise RuntimeError('Expected 32 V-base exterior edges, found %d' % len(exterior_edges))
    features.append(_add_handle_fillet(
        component, exterior_edges, '1.5 mm',
        'HANDLE_ALL_V_BASE_EXTERIOR_EDGES_R1_5', True
    ))

    def horizontal_circle_edges(radius_mm, z_mm):
        matches = []
        current_body = component.bRepBodies.item(0)
        for edge in current_body.edges:
            circle = adsk.core.Circle3D.cast(edge.geometry)
            if not circle or abs(circle.radius * 10 - radius_mm) > 0.05:
                continue
            bb = edge.boundingBox
            z0, z1 = bb.minPoint.z * 10, bb.maxPoint.z * 10
            if abs(z0 - z_mm) < 0.1 and abs(z1 - z_mm) < 0.1:
                matches.append(edge)
        if len(matches) != 4:
            raise RuntimeError(
                'Expected four R%.2f circle edges at Z%.1f, found %d' %
                (radius_mm, z_mm, len(matches))
            )
        return matches

    features.append(_add_handle_fillet(
        component, horizontal_circle_edges(3.15, HANDLE_BASE_Z1),
        '0.6 mm', 'HANDLE_M3_COUNTERBORE_ENTRY_EDGES_R0_6'
    ))
    features.append(_add_handle_fillet(
        component, horizontal_circle_edges(4.45, 222.4),
        '0.3 mm', 'HANDLE_LOCATOR_LEAD_EDGES_R0_3'
    ))
    features.append(_add_handle_fillet(
        component, horizontal_circle_edges(1.7, 222.4),
        '0.3 mm', 'HANDLE_M3_EXIT_EDGES_R0_3'
    ))
    return features


def build_rect_bottom_cap(tb):
    body = base.rounded_prism(tb, CAP_WIDTH, CAP_DEPTH, CAP_RADIUS, 0, 8)
    groove = base.rounded_ring(tb, 133.5, 97.5, 7.25, 2.5, 5.0, 8.5)
    base.cut(tb, body, groove, 'rect-bottom-cap-sleeve-groove')

    for x in (-45.0, 45.0):
        for y in (-35.0, 35.0):
            base.cut(tb, body, base.make_cyl(tb, x, y, -1, x, y, 18, 1.7), 'bottom-m3-clearance')
            base.cut(tb, body, base.make_cyl(tb, x, y, -0.5, x, y, 3.0, 3.2), 'bottom-m3-head-recess')

    for x, y in RUBBER_FOOT_POSITIONS:
        base.cut(tb, body, base.make_cyl(tb, x, y, -0.2, x, y, 0.8, 5.0), 'rubber-foot-pocket')
        # Preserve the baseline's later Extrude1: each Ø10 pocket face was
        # joined downward by 5 mm, producing a foot from Z -4.2 to +0.8.
        base.unite(tb, body, base.make_cyl(tb, x, y, -4.2, x, y, 0.8, 5.0), 'integrated-bottom-foot')
    return body
