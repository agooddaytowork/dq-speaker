# SPEC — Concept case loa dạng Sonos One

**Trạng thái:** Draft để duyệt trước khi dựng CAD  
**Phiên bản:** 1.9 — correct red-edge column pair shift; front columns Ø4.2 mm  
**Ngày:** 2026-08-26  
**Đơn vị mặc định:** mm  
**Nguồn tham chiếu Fusion 360:** `TEST-BACK2-SONOS-ONE-SL-ROUNDED-V6`

> Quy ước trong tài liệu: **CHỐT** = yêu cầu đã có từ brief; **ĐỀ XUẤT** = giá trị khởi đầu để dựng concept; **CẦN DUYỆT** = cần xác nhận hoặc sửa trước khi làm CAD chính thức.

## 1. Các mục cần duyệt nhanh

Sửa trực tiếp bảng này trước khi bắt đầu dựng model.

| Hạng mục | Giá trị draft | Trạng thái / ghi chú |
|---|---:|---|
| Dáng tổng thể | Trụ bo góc kiểu Sonos One, tiết diện rounded-square | **ĐỀ XUẤT**; không hiểu là hình trụ tròn tuyệt đối |
| Kích thước ngoài mục tiêu | 135 W × 135 D × 224 H | **ĐỀ XUẤT**, tăng top cap từ 8 lên 12 |
| Số nhóm chức năng chính | 4 | **CHỐT**: frame, sleeve, top cap, bottom cap |
| Số part in thực tế | 9 | **CHỐT**: front frame, rear frame, sleeve, top cap, 4 top screw plugs, bottom cap |
| Màu khung | Không yêu cầu; dùng màu PETG sẵn có | **CHỐT** |
| Màu thân ngoài | Xám | **CHỐT** |
| Màu mặt trên | Cam | **CHỐT** |
| Màu mặt dưới | Cam | **CHỐT** |
| Lỗ power trên mặt trên | Ø13.0 xuyên suốt | **CHỐT** |
| Lỗ USB-C trên mặt trên | Ø11.0 xuyên suốt | **CHỐT** |
| Khoảng cách tâm 2 lỗ | 16.0 | **ĐỀ XUẤT**, lấy từ V6 hiện tại |
| Vật liệu prototype | PETG Bambu Lab | **CHỐT**; profile in theo đúng mã filament thực tế |
| Vít kết cấu chính | M3 × 16 mm | **CHỐT**, đang có sẵn |
| Vít phụ | M2 × 10 mm | **CHỐT là phần cứng có sẵn**, dùng khi phù hợp |
| Insert ren | Heat-set insert M3 và M2 đang có sẵn | **CHỐT loại ren**, cần đo OD/chiều dài insert thực tế |
| Kiểu bắt vít ngoài | Vít M3 thao tác từ đáy và từ mặt trên; mỗi vít trên có một plug tháo được | **CHỐT** |
| Mặt dưới | Đáy tháo được, có chân cao su | **ĐỀ XUẤT** |
| Phạm vi lỗ thoát âm | Quấn qua mặt phẳng và cả bốn góc bo; chỉ chừa spine kín phía sau | **CHỐT** |

## 2. Mục tiêu sản phẩm

Thiết kế một case loa mới có ngôn ngữ hình khối gợi nhớ Sonos One: thân đứng, bo góc lớn, bề mặt xám có pattern lỗ thoát âm, nắp trên và nắp dưới màu cam.

Thiết kế mới phải:

1. Tái sử dụng chính xác các interface đã fit-test thành công từ hai component V6 hiện tại.
2. Tách chức năng gá linh kiện khỏi vỏ trang trí bên ngoài.
3. Gồm bốn nhóm chức năng: `FRAME_ASSEMBLY`, `OUTER_SLEEVE`, `TOP_CAP`, `BOTTOM_CAP`; frame assembly gồm hai part in và top cap có bốn plug che vít in riêng.
4. `FRONT_FRAME` và `REAR_FRAME` lắp vào loa từ hai phía rồi ghép tại bốn joint ngoại vi; không có joint xuyên qua acoustic keepout ở giữa loa.
5. Sleeve ăn khớp với groove trên top/bottom cap và được hai cap ép giữ; sleeve không dùng vít xuyên trực tiếp.
6. Tháo lắp được bằng vít M3/M2 và heat-set insert tương ứng, không dùng keo làm liên kết kết cấu chính.
7. Có cấu trúc parametric, dễ thay đổi kích thước và pattern trước khi xuất file in.

## 3. Phạm vi

### 3.1 Trong phạm vi

- Dựng concept cơ khí hoàn chỉnh trong Fusion 360.
- Chuyển các mounting holes phía sau và mounting columns phía trước thành hai nửa frame lắp từ hai phía; các nửa chỉ liên kết qua vùng biên.
- Dựng thân ngoài có pattern lỗ thoát âm.
- Dựng nắp trên dày 12, chứa hai lỗ cổng, bốn lỗ vít M3 thao tác từ trên và logo `DQ` nổi ở thành trước.
- Dựng bốn plug PETG cam tháo được, mỗi plug chỉ che đúng một đầu vít top cap; không dùng cover toàn mặt.
- Dựng nắp dưới tháo được.
- Thiết kế interface vít M3/M2, insert, khe hở lắp ghép và chống xoay/lắp ngược.
- Kiểm tra interference, khả năng lắp ráp và khả năng in FDM.
- Xuất STEP và STL cho chín part vật lý sau khi thiết kế được duyệt; bốn plug có thể dùng chung một file STL mẫu.

### 3.2 Ngoài phạm vi ở vòng concept đầu

- Thay đổi vị trí phần cứng đã fit-test.
- Thiết kế lại PCB, driver, nút power hoặc đầu nối USB-C.
- Tối ưu âm học bằng mô phỏng SPL/CFD.
- Thiết kế khuôn ép nhựa.
- Sao chép chính xác hình dáng hoặc pattern thương mại của Sonos.

## 4. Baseline đã kiểm tra từ Fusion 360

### 4.1 Hai reference chính

| Reference V6 | Vai trò dùng trong thiết kế mới | Bounding box đo trong Fusion |
|---|---|---:|
| `Body1_REAR_MOUNTING_ROUNDED_PRODUCTION_V6:1` | Nguồn chuẩn cho mounting phía sau và vị trí hai cổng | 125.0 × 196.5 × 53.0 |
| `Fit_Test_FRONT_4MM_PINS_ROUNDED_PRODUCTION_V6:1` | Nguồn chuẩn cho các cột/pin mounting phía trước | 125.0 × 196.5 × 44.0 |

Envelope tổng khi hai phần ở vị trí lắp hiện tại xấp xỉ **125.0 W × 196.5 H × 94.0 D**.

### 4.2 Nguyên tắc giữ chuẩn fit-test

- Hai component trên là **master reference**, không được sửa trực tiếp.
- Khi dựng file mới, đưa chúng vào group `00_REFERENCE_DO_NOT_EDIT` và khóa vị trí.
- Geometry chức năng phải được project/derive từ reference, không vẽ lại bằng mắt.
- Tọa độ đo dưới đây chỉ dùng để audit; geometry gốc trong Fusion là nguồn chuẩn cuối cùng.
- Không scale reference theo bất kỳ trục nào.
- Không thay đổi khoảng cách, đường kính hoặc chiều dài mounting feature nếu chưa có fit-test mới.

### 4.3 Các feature đo được để audit

Trong hệ tọa độ nguồn hiện tại:

- Cụm phía sau có bốn lỗ ứng viên Ø3.0, đồng tâm với boss Ø6.0 tại các vị trí XY: `(0, 0)`, `(97, 0)`, `(0, -61)`, `(97, -61)`.
- Reference V6 có sáu cột trụ Ø5.0 tại các vị trí XY: `(0, 0)`, `(97, 0)`, `(0, -61)`, `(97, -61)`, `(1.5, -102)`, `(95.5, -102)`; chiều dài hình học đo được khoảng 31.5.
- Trên `FRONT_FRAME` mới, giữ nguyên chiều dài của sáu cột nhưng đặt đường kính danh nghĩa **Ø4.2 mm**; boss chân vẫn Ø8.0 mm.
- Cặp tại product coordinate `X = ±48.5, Z = 165.25 mm` được trả đúng về vị trí V6; cặp giữa `X = ±48.5, Z = 104.25 mm` cũng giữ nguyên như V6.
- Chỉ cặp phía cạnh đỏ tại `X = ±47.0, Z = 63.25 mm` được dịch 5 mm theo `-Z`, đưa tâm mới tới `Z = 58.25 mm`.
- Bốn cột mounting-hole chính trên `REAR_FRAME` có đường kính ngoài giảm từ Ø8.0 xuống **Ø6.0 mm**; lỗ xuyên giữ Ø3.0 mm, tâm và chiều dài cột không đổi.
- Model V6 có hai lỗ cổng cách tâm 16.0. Lỗ USB-C đo được Ø11.0; lỗ power trong model đo được khoảng Ø12.0.
- Yêu cầu mới **ghi đè** đường kính power của V6: dùng Ø13.0 cho `TOP_CAP`.

Trước khi tạo feature mới, người dựng CAD phải xác nhận trực quan từng feature trên model để phân biệt lỗ chức năng, boss và bề mặt bo; không suy luận chỉ từ bounding box.

## 5. Kiến trúc bốn nhóm chức năng / chín part vật lý

### 5.1 `01_FRAME_ASSEMBLY`

Frame assembly gồm `01A_REAR_FRAME` và `01B_FRONT_FRAME`. Hai nửa được đưa vào loa từ hai phía theo đúng hướng lắp của mounting holes/columns, sau đó ghép bằng bốn vít M3 × 16 tại các rail ngoài vùng loa.

Mỗi nửa frame gồm:

- Ring ngoại vi trên/dưới thuộc mặt front hoặc rear tương ứng.
- Hai rail dọc trái/phải nối trực tiếp top–bottom.
- Các arm ngắn cục bộ từ rail biên tới bộ mounting tương ứng.
- Bốn trụ nối theo chiều sâu thuộc hoàn toàn về `FRONT_FRAME`; không chia đôi trụ và không dựng hai arm đối đầu nhau.
- `REAR_FRAME` chỉ có bốn boss nhận insert nhỏ, tích hợp trực tiếp vào rail sau tại đầu mỗi trụ.
- Boss insert M3 ở cả đáy và đầu trên; không dùng vít ẩn phía trong cho top cap.
- Khe đi dây và strain-relief không có cạnh sắc.

Yêu cầu bắt buộc:

- Không có joint, pin định vị, tie-rod, crossbar hoặc vít nào nối front–rear bằng cách xuyên qua vùng giữa loa.
- Acoustic keepout trung tâm phải thông suốt. Keepout draft: vùng `105 W × 70 D`, từ Z=25 tới Z=195; chỉ mounting feature V6 thực sự bắt buộc mới được đi vào vùng này.
- Bốn trụ nối đặt sát hai hông, tâm `X ≈ ±61`, `Z ≈ 18/202`; trụ chạy từ front rail tới mặt nhận phía sau `Y ≈ -31` và nằm ngoài acoustic keepout theo X/Z.
- Joint chỉ chồng lắp cục bộ tại đầu sau của trụ. Không có arm thứ hai chạy từ `REAR_FRAME` vào giữa loa.
- Vít joint chạy dọc theo X và được đưa tua-vít từ mặt hông sau khi tháo sleeve; không đặt đầu vít tại seam bên trong.
- Terminal pad của trụ thuộc `FRONT_FRAME` chứa lỗ clearance Ø3.4 và counterbore đầu vít Ø6.2 sâu khoảng 3.5; đầu vít nằm flush hoặc thấp hơn mặt X=±64.
- Boss nhận thuộc `REAR_FRAME` chứa pilot Ø4.2 cho insert M3, không có arm kéo dài; insert được ép trước khi ráp.
- Terminal pad và boss insert xếp nối tiếp theo trục vít, tổng screw stack danh nghĩa 16; vít không được bottom-out.
- Mặt cuối trụ tạo datum cục bộ với boss nhận; không dùng pin ở tâm.
- Mounting holes/columns giữ đúng datum V6; support arm phải đi về phía rail gần nhất thay vì bắc ngang toàn chiều rộng.
- Spine chứa hai mounting M2 trung tâm của `REAR_FRAME` phải overlap bottom rail tối thiểu 0.5; không được tồn tại như một island hình học.
- Không được che mặt phát âm hoặc vùng thông khí chức năng của phần cứng.
- Khoảng hở tĩnh tới linh kiện: tối thiểu 1.0; quanh dây/cổng cắm: tối thiểu 1.5.
- Rail dọc chính: tiết diện khởi đầu 6 × 8; rib cục bộ dày 1.6–2.0 và fillet chân R1.0 trở lên.
- Bốn junction rail ngang–dọc trên mỗi half-frame có fillet lõm, tiếp tuyến R3; không dùng cylinder/gusset lồi tại tâm góc và không vượt outer envelope hiện tại.
- Chân bốn tie-post trên `FRONT_FRAME` và chân bốn insert receiver trên `REAR_FRAME` có fillet lõm R2 ở cả hai cạnh chân để giảm tập trung ứng suất và nguy cơ tách layer PETG.
- Tất cả junction 90° chịu lực còn lại giữa mounting arm/service spine và rail phải có fillet lõm R1.5: 14 cạnh trên `REAR_FRAME`, 12 cạnh trên `FRONT_FRAME`.
- Các bo R3/R2/R1.5 phải được tạo bằng `FilletFeature` native của Fusion trên edge-set đã audit; không dựng lại cung bo bằng box/cylinder/boolean thủ công.
- Không bo các cạnh chuẩn chức năng tại miệng lỗ, insert seat, đầu pin và mặt datum ép nắp; các cạnh này phải giữ nguyên để bảo toàn fit-test hiện tại.
- Không bo vào clearance hole, counterbore hoặc pilot insert; thành vật liệu quanh lỗ vẫn phải đạt tối thiểu 2.0.
- Boss insert M3: OD danh nghĩa tối thiểu 8.0, có gusset.
- Hai nửa phải tháo lắp được sau khi bỏ sleeve và cap; không dùng keo.
- Sau khi ráp, frame assembly tạo load path top–bottom qua bốn rail dọc ngoại vi.
- Mỗi half-frame phải audit `BRepBody.lumps.count = 1` trước khi lưu hoặc xuất STL; việc nhiều feature nằm trong cùng tên body không được coi là đã liên kết.

### 5.2 `02_OUTER_SLEEVE_GREY`

Thân ngoài là một sleeve mở hai đầu, tiết diện rounded-square và có pattern lỗ thoát âm.

Giá trị hình học khởi đầu:

- Kích thước ngoài: 133 × 133 để chừa outer lip trên cap 135 × 135.
- Chiều cao sleeve nhìn thấy: 204.
- Chiều cao part thực: 209, gồm 2.5 ăn vào groove ở mỗi đầu.
- Corner radius ngoài: R27.
- Bề dày thành danh nghĩa: 2.0.
- Draft cho FDM: 0°; không thêm draft khuôn ép ở vòng này.
- Seam với nắp trên/dưới: 0.5–0.8 nhìn thấy, đồng đều quanh chu vi.

Pattern đề xuất, kế thừa ngôn ngữ của V6 nhưng không sao chép Sonos:

- Dạng capsule ngang, đầu tròn.
- Kích thước slot khởi đầu: dài tổng 5.4 × rộng 2.2.
- Bước hàng dọc: 6.0.
- Bước cột trong cùng một hàng: 10.0.
- Hàng kế tiếp stagger 5.0 theo phương ngang.
- Tỷ lệ diện tích mở mục tiêu: 16–20% trong acoustic zone.
- Chừa vành kín tối thiểu 10 ở đầu trên và đầu dưới.
- Chừa vùng kín quanh boss/vít tối thiểu 6 tính từ mép lỗ.
- Chừa một rear service spine rộng 24–30 để tăng cứng, che rail và tránh nhìn xuyên vào dây.
- Pattern phải wrap liên tục qua toàn bộ bốn góc R27; không để lại dải góc kín chạy dọc chiều cao.
- Slot tại góc đặt theo tiếp tuyến bề mặt, cutter đi theo phương bán kính qua thành sleeve.
- Pitch góc danh nghĩa 18°; hàng Z xen kẽ 4/5 slot trên mỗi góc để giữ stagger tại vùng chuyển flat–curve.
- Không để slot bị cắt thành mảnh mỏng dưới 1.2.

Yêu cầu cơ khí:

- Sleeve trượt qua frame assembly đã ráp mà không cần ép mạnh.
- Có key bất đối xứng để chống xoay 180°.
- Mép trên và dưới của sleeve ăn vào groove rounded-ring trên hai cap, sâu danh nghĩa 2.5.
- Sleeve không bắt vít trực tiếp. Bottom cap được siết vào frame sẽ ép sleeve về phía top cap và giữ sleeve bằng hai groove.
- Groove có radial clearance 0.25 mỗi bên và axial clearance mục tiêu 0.15–0.25 sau coupon; không tạo preload CAD cưỡng bức gây interference.
- Không có vít lộ trên mặt trước hoặc hai bên ở concept mặc định.

### 5.3 `03_TOP_CAP_ORANGE`

Nắp trên màu cam, có groove nhận mép sleeve và liên kết ẩn với đầu trên của frame.

Yêu cầu:

- Kích thước ngoài đồng profile 135 × 135, corner radius R28.
- Phần nhìn thấy cao khoảng 8.
- Top skin dày danh nghĩa 3.0.
- Groove rounded-ring rộng danh nghĩa 2.5, sâu 3.0; mép sleeve ăn vào 2.5.
- Radial clearance groove/sleeve: 0.25 mỗi bên cho PETG FDM.
- Top cap dày danh nghĩa 12, từ Z=212 tới Z=224 trong hệ tọa độ concept.
- Top cap bắt vào frame bằng bốn vít M3 × 16 đưa từ mặt trên xuống; bố trí đối xứng tại `X = ±45`, `Y = ±35`.
- Lỗ clearance vít Ø3.4 và counterbore đầu vít Ø6.4; đỉnh đầu vít phải nằm thấp hơn đáy pocket plug ít nhất 0.1.
- Frame có bốn boss insert M3 tương ứng, hai boss trên mỗi half-frame; insert được ép vào frame trước khi lắp cap.
- Trên top cap có bốn pocket tròn Ø9.2 sâu 1.7, mỗi pocket nhận một screw plug Ø8.9 × 1.6 và lắp flush với mặt trên.
- Thành trước `+Y` của top cap có monogram `DQ` hình học bo tròn nổi 0.8, kích thước tổng thể khoảng 20 W × 8.4 H. `D` dùng vòng cung và sống thẳng; `Q` dùng vòng tròn cùng độ dày nét với đuôi chéo ngắn. Không dùng block-letter góc vuông.
- Lực từ frame truyền vào top cap qua bốn vít M3, không truyền qua thành sleeve bằng vít.
- Lỗ power: **Ø13.0 xuyên suốt**.
- Lỗ USB-C: **Ø11.0 xuyên suốt**.
- Hai lỗ giữ đúng vị trí tương quan với phần cứng; khoảng cách tâm baseline 16.0.
- Vát mép ngoài lỗ 0.5 × 45° hoặc fillet R0.5 để dễ cắm và không sắc cạnh.
- Chừa clearance phía dưới quanh thân đầu cắm/nút ít nhất 1.0 theo mọi hướng.
- Không tự động đặt hai lỗ vào giữa nắp. Vị trí cuối phải derive từ phần cứng đã fit-test sau khi chuẩn hóa hệ trục assembly.

### 5.3.1 `03B_TOP_SCREW_PLUGS_ORANGE`

- Gồm bốn plug PETG cam giống nhau, mỗi plug Ø8.9 × 1.6 và chỉ phủ một counterbore M3.
- Plug được giữ bằng ma sát chu vi trong pocket Ø9.2; không thuộc load path kết cấu.
- Mỗi plug/pocket có pry scallop R0.8–0.9 hướng ra phía biên gần nhất để tháo bằng dụng cụ nhựa mỏng.
- Khe hở xuyên tâm khởi đầu 0.15; phải in coupon để chốt theo profile PETG thực tế.
- Hai lỗ USB-C/power nằm trực tiếp trên top cap cam, không đi qua một cover lớn.
- Mặt ngoài không có support scar trong hướng in được chọn.

### 5.4 `04_BOTTOM_CAP_ORANGE`

Nắp dưới màu cam là service cover và là điểm tháo chính của assembly.

Đề xuất mặc định:

- Kích thước ngoài đồng profile 135 × 135, corner radius R28.
- Phần nhìn thấy cao khoảng 8.
- Bottom skin dày 3.0.
- Groove rounded-ring rộng danh nghĩa 2.5, sâu 3.0; radial clearance 0.25 mỗi bên.
- Bốn vít M3 × 16 đi từ mặt đáy vào insert trên `FRAME_ASSEMBLY`; khi siết, bottom cap ép sleeve vào groove của top cap.
- Lỗ vít clearance Ø3.4; counterbore/countersink chỉ chốt sau khi chọn loại đầu vít.
- Bốn vị trí chân cao su, đường kính pad 8–12, cao 1.5–3.0.
- Chân tạo khoảng hở tối thiểu 1.5 giữa đầu vít và mặt bàn.
- Có notch nhỏ hoặc finger relief để tháo cap sau khi tháo vít.
- Không có lỗ thoát nước ở bản mặc định vì sản phẩm không được xác định là chống nước.

**CẦN DUYỆT:** có cần lỗ dây, tem nhãn, QR/serial, lỗ tripod hoặc bass port ở đáy hay không.

## 6. Liên kết vít và heat-set insert

### 6.1 Liên kết M3 chính

- Ren danh nghĩa: M3 × 0.5.
- Phần cứng có sẵn: vít M3 × 16.
- Cụm ghép frame ngoại vi: 4 vít M3 × 16 và 4 insert M3.
- Cụm đáy/case: 4 vít M3 × 16 tháo từ đáy và bắt vào 4 insert M3 trên frame assembly.
- Cụm top cap: 4 vít M3 × 16 tháo từ mặt trên và bắt vào 4 insert M3 trên frame assembly; bốn plug chỉ che từng đầu vít.
- Tổng nhu cầu concept mặc định: 12 vít M3 × 16 và 12 insert M3, chưa gồm linh kiện dự phòng.
- Insert tham chiếu ban đầu: OD khoảng 4.6, dài khoảng 5.7; **phải thay bằng kích thước đo/datasheet của insert thực có**.
- Pilot hole khởi đầu cho insert: Ø4.1–4.3, có lead-in 0.5 × 45°.
- Chiều dày vật liệu quanh insert theo bán kính: tối thiểu 1.5; ưu tiên boss OD ≥8.0.
- Screw stack phải được thiết kế riêng cho vít dài 16: sau khi qua bottom cap và washer/counterbore nếu có, chiều dài ăn ren mục tiêu 5–8.
- Phải chừa khoảng an toàn tối thiểu 1.0 giữa đầu vít và đáy lỗ insert; vít tuyệt đối không bottom-out.
- Nếu stack danh nghĩa quá ngắn cho vít 16, tăng chiều cao standoff hoặc dùng spacer tích hợp; không để vít xuyên vào vùng linh kiện.
- Mô-men siết thử nghiệm ban đầu: 0.3–0.5 N·m, sau đó kiểm tra nứt boss và tuột insert.

### 6.2 Liên kết M2 phụ

- Ren danh nghĩa: M2 × 0.4.
- Phần cứng có sẵn: vít M2 × 10 và heat-set insert M2.
- M2 được dự phòng cho cable clamp hoặc chi tiết tải nhẹ cần tiết kiệm không gian.
- Top cap không còn dùng M2 trong revision 0.6 vì vít ẩn phía trong không có đường thao tác hợp lệ.
- Không dùng M2 làm bốn vít kết cấu chính ở đáy và không dùng tại load path chịu va đập của toàn case.
- Pilot hole, boss OD, chiều sâu insert và screw stack phải dựng theo kích thước insert M2 thực tế; chưa khóa bằng giá trị generic trong bản spec này.
- Chiều dài ăn ren mục tiêu: 3–5; chừa tối thiểu 0.8 trước đáy lỗ và không để vít bottom-out.
- Mô-men siết phải thấp hơn M3 và được xác định bằng test coupon để tránh xoay insert hoặc nứt PETG.

### 6.3 Yêu cầu chung

- Tất cả screw axis service phải tiếp cận được sau khi tháo bottom cap.
- Dùng insert theo đúng loại ren; không thiết kế một boss dùng chung cho cả M2 và M3.
- Tạo coupon riêng cho boss M2 và M3 bằng PETG Bambu Lab trước khi in frame đầy đủ.

## 7. Kích thước và tham số Fusion 360 đề xuất

File concept mới phải là parametric design. Không dựng tiếp trong direct-design source V6.

| User parameter | Giá trị draft | Ý nghĩa |
|---|---:|---|
| `caseWidth` | 135 mm | Kích thước trái–phải |
| `caseDepth` | 135 mm | Kích thước trước–sau |
| `caseHeight` | 224 mm | Tổng chiều cao sản phẩm sau khi tăng top cap |
| `cornerRadius` | 28 mm | Bo góc profile ngoài |
| `sleeveWall` | 2.0 mm | Thành thân xám |
| `sleeveOuterSize` | 133 mm | Kích thước ngoài sleeve, cap vẫn 135 |
| `sleeveVisibleHeight` | 204 mm | Chiều cao thân xám nhìn thấy |
| `sleevePrintedHeight` | 209 mm | Chiều cao part gồm hai mép vào groove |
| `topCapVisibleHeight` | 12 mm | Phần cam kết cấu nhìn thấy ở đầu trên |
| `bottomCapVisibleHeight` | 8 mm | Phần cam nhìn thấy ở đáy |
| `topScrewPlugThickness` | 1.6 mm | Chiều dày mỗi plug vít nằm flush |
| `topScrewPlugDia` | 8.9 mm | Đường kính mỗi plug che counterbore M3 |
| `capSkin` | 3.0 mm | Bề dày mặt cap |
| `grooveDepth` | 3.0 mm | Chiều sâu groove trên mỗi cap |
| `sleeveEngagement` | 2.5 mm | Độ ăn mép sleeve vào mỗi groove |
| `grooveRadialClearance` | 0.25 mm | Clearance mỗi bên của groove |
| `seamGap` | 0.6 mm | Khe shadow line cap/sleeve |
| `ventSlotLength` | 5.4 mm | Dài tổng capsule |
| `ventSlotWidth` | 2.2 mm | Rộng capsule |
| `ventPitchX` | 10 mm | Pitch ngang cùng hàng, pattern dày |
| `cornerVentRadius` | 27 mm | Bán kính tâm slot trên bốn góc bo |
| `cornerVentAngularPitch` | 18° | Pitch góc danh nghĩa của slot tiếp tuyến |
| `rearSpineWidth` | 27 mm | Dải kín phía sau |
| `powerCutoutDia` | 13 mm | Lỗ power mới |
| `usbCutoutDia` | 11 mm | Lỗ USB-C mới |
| `portCenterPitch` | 16 mm | Khoảng cách tâm baseline |
| `m3ClearanceDia` | 3.4 mm | Lỗ clearance vít M3 |
| `insertPilotDia` | 4.2 mm | Giá trị thử, đổi theo insert |
| `m3ScrewLength` | 16 mm | Chiều dài vít M3 có sẵn |
| `m2ClearanceDia` | 2.4 mm | Lỗ clearance M2 khởi đầu |
| `m2ScrewLength` | 10 mm | Chiều dài vít M2 có sẵn |
| `m2InsertPilotDia` | TBD | Đo theo insert M2 thực tế |
| `frameRailWidth` | 6 mm | Bề rộng rail dọc ngoại vi |
| `frameRailDepth` | 8 mm | Chiều sâu rail dọc ngoại vi |
| `frameMainCornerFillet` | 3 mm | Bo trong junction rail ngang–dọc |
| `frameJointRootFillet` | 2 mm | Bo chân tie-post và insert receiver |
| `framePeripheralJointX` | 64 mm | Mặt hông có counterbore, tháo sleeve để tiếp cận |
| `frontMountingColumnDia` | 4.2 mm | Đường kính danh nghĩa của sáu mounting columns mặt trước |
| `frontRedEdgeColumnShiftZ` | -5 mm | Chỉ dịch cặp `X = ±47` về cạnh đỏ theo -Z |
| `rearMountingBossDia` | 6 mm | Đường kính ngoài bốn cột mounting-hole chính trên rear frame |
| `frameJointScrewCount` | 4 | Số joint M3 ngoại vi |
| `acousticKeepoutWidth` | 105 mm | Keepout trung tâm theo X |
| `acousticKeepoutDepth` | 70 mm | Keepout trung tâm theo Y |
| `minHardwareClearance` | 1.0 mm | Hở tĩnh tối thiểu |

Kích thước 135 × 135 × 224 chỉ được freeze sau khi chạy section/interference với toàn bộ reference. Nếu clearance thực tế nhỏ hơn yêu cầu, tăng case theo bước 2 mm; không scale hoặc dịch mounting geometry để ép vừa.

## 8. Cấu trúc file Fusion 360

```text
SONOS_CASE_CONCEPT_V1
├── 00_REFERENCE_DO_NOT_EDIT
│   ├── REF_REAR_V6
│   └── REF_FRONT_V6
├── 01_FRAME_ASSEMBLY
│   ├── 01A_REAR_FRAME
│   └── 01B_FRONT_FRAME
├── 02_OUTER_SLEEVE_GREY
├── 03_TOP_CAP_ORANGE
├── 03B_TOP_SCREW_PLUGS_ORANGE
│   ├── TOP_SCREW_PLUG_01
│   ├── TOP_SCREW_PLUG_02
│   ├── TOP_SCREW_PLUG_03
│   └── TOP_SCREW_PLUG_04
├── 04_BOTTOM_CAP_ORANGE
└── 90_HARDWARE_CHECK
    ├── M3_SCREWS
    ├── M3_INSERTS
    ├── M2_SCREWS
    ├── M2_INSERTS
    └── RUBBER_FEET
```

Quy tắc model:

- Mỗi part sản xuất là một component riêng và có một main solid body ở trạng thái release.
- Sketch phải fully constrained, đặt tên theo chức năng.
- Không dùng projection mất liên kết cho interface fit-test.
- Pattern lỗ phải dùng pattern feature hoặc script có tham số; không tạo hàng trăm feature rời không quản lý được.
- Tạo construction planes cho `TOP_DATUM`, `BOTTOM_DATUM`, `FRONT_DATUM`, `REAR_DATUM` và `PORT_AXIS`.
- Gán appearance xám/cam chỉ để review; màu file không thay thế chỉ định vật liệu.
- Source V6 đang là direct design; phải tạo concept trong file mới hoặc copy có timeline parametric.

## 9. DFM cho prototype FDM

- Nozzle tham chiếu: 0.4.
- Layer height tham chiếu: 0.20.
- Thành chịu lực: tối thiểu 3 perimeter với slicer thực tế.
- Feature mỏng tuyệt đối không dưới 1.2; ưu tiên bội số phù hợp line width.
- Bridge không support mục tiêu: ≤8 đối với bề mặt cần đẹp; dùng chamfer 45° thay overhang ngang khi có thể.
- Fillet ngoài tối thiểu R0.8 tại vùng cầm nắm; chân rib/boss R1.0–1.5.
- Lỗ in theo phương ngang cần compensation hoặc profile teardrop nếu độ tròn ảnh hưởng lắp ghép.
- In coupon gồm: groove/sleeve clearance, lỗ Ø11/Ø13 và boss insert M3/M2 trước khi in full-size.
- Vật liệu prototype: PETG Bambu Lab. Chọn đúng profile theo mã filament trên spool (ví dụ dòng PETG cụ thể), sấy và hiệu chuẩn flow/pressure advance theo quy trình in thực tế.
- Màu của hai nửa `FRAME_ASSEMBLY` không bị ràng buộc; có thể dùng bất kỳ màu PETG Bambu Lab nào đang có.
- Hướng in và support phải được ghi trong manifest xuất file.

## 10. Âm học và thông khí

- `OUTER_SLEEVE` là lớp bảo vệ/trang trí có lỗ; không được giả định nó là acoustic chamber kín.
- Giữ nguyên acoustic volume và sealing surface của cụm đã fit-test, trừ khi có yêu cầu âm học mới.
- Không đặt rail, boss, insert hoặc dây chắn trực tiếp phía sau vùng thoát âm chính.
- Khoảng hở từ mặt trong sleeve tới phần chuyển động của driver phải được kiểm tra ở hành trình cực đại; khi chưa có excursion data, dùng tối thiểu 3.0.
- Tổng open area của sleeve phải được báo cáo sau khi pattern; mục tiêu draft 16–20% trong vùng perforated.
- Sau prototype phải kiểm tra tiếng rattle/buzz ở sweep 40 Hz–20 kHz theo mức âm lượng sử dụng thực tế.

## 11. Trình tự lắp ráp mục tiêu

1. Ép nhiệt toàn bộ insert M3 vào frame bằng jig vuông góc.
2. Đưa `REAR_FRAME` vào bộ mounting phía sau và `FRONT_FRAME` vào mounting columns từ phía trước.
3. Đưa bốn trụ của `FRONT_FRAME` dọc sát hông tới boss insert tích hợp của `REAR_FRAME`; siết bốn vít M3 × 16 từ hai mặt hông theo thứ tự chéo góc.
4. Kiểm tra acoustic keepout, đi dây và strain relief.
5. Trượt `OUTER_SLEEVE_GREY` qua frame, đưa mép trên vào groove của top cap.
6. Lắp `TOP_CAP` và siết bốn vít M3 × 16 từ mặt trên theo thứ tự chéo góc; xác nhận nút/cổng không cấn.
7. Ấn bốn `TOP_SCREW_PLUG` vào đúng bốn pocket; xác nhận từng plug flush và pry scallop tiếp cận được.
8. Đưa groove của `BOTTOM_CAP_ORANGE` vào mép dưới sleeve.
9. Siết bốn vít M3 × 16 từ đáy theo thứ tự chéo góc; bottom cap ép sleeve về phía top cap.
10. Gắn chân cao su, kiểm tra hai seam và độ cập kênh.

Assembly phải tháo ngược được mà không phá part, không tháo insert và không cần bóc keo.

## 12. Tiêu chí nghiệm thu CAD

### 12.1 Geometry

- Có chín part vật lý; frame assembly gồm hai solid body front/rear và bốn top screw plug là các part tháo rời.
- Hai reference V6 được giữ nguyên vị trí và hình học.
- Vị trí tương quan giữa bộ mounting holes và mounting columns trùng với V6 trong dung sai 0.20 tại các datum chức năng.
- Không có frame member hoặc fastener không bắt buộc đi xuyên acoustic keepout trung tâm.
- Interference analysis không có va chạm giữa hardware, frame, sleeve và hai cap.
- Clearance lắp trượt đạt 0.25 mỗi bên tại trạng thái danh nghĩa.
- Không có zero-thickness face, self-intersection hoặc body không kín.
- Power cutout = Ø13.0; USB-C cutout = Ø11.0.
- Hai cổng thẳng trục với hardware thực/geometry reference.

### 12.2 Lắp ráp

- Lắp được bằng dụng cụ tay thông thường.
- Không cần lực ép làm biến dạng sleeve.
- Không thể lắp sleeve sai chiều nếu không dùng lực bất thường.
- Toàn bộ vít service tiếp cận từ đáy theo concept mặc định.
- Không có đầu vít lộ ở mặt trước và hai bên.

### 12.3 In thử và fit-test

- In coupon groove trước, sau đó in vùng mounting và một joint ngoại vi cắt ngắn; chỉ in full frame sau khi interface pass.
- Pin/cột phía trước và hole/boss phía sau phải pass lại cùng phần cứng đã dùng ở V6.
- Nút power thao tác không kẹt; đầu USB-C cắm hết hành trình và rút được bằng tay.
- Insert M3 không xoay hoặc tuột ở 0.5 N·m; insert M2 phải đạt mô-men test riêng được xác lập bằng coupon.
- Case đứng phẳng; bốn chân chạm mặt bàn.
- Không rattle/buzz rõ ràng trong bài test sweep.

## 13. Deliverables sau khi duyệt spec

- Fusion 360 design parametric có cấu trúc component đúng mục 8, gồm chín part vật lý.
- Một assembly view và một exploded view.
- Section view thể hiện hardware clearance và screw/insert stack.
- Bảng user parameters cuối cùng.
- Interference report.
- Chín part vật lý: rear frame, front frame, sleeve, top cap, bốn top screw plug và bottom cap; bốn plug có thể xuất từ cùng một STL mẫu.
- STEP cho từng part và STEP toàn assembly.
- BOM phần cứng mặc định: 12 × M3 × 16, 12 insert M3 và chân cao su; M2 × 10/insert M2 được giữ làm phần cứng dự phòng.
- Manifest ghi revision, vật liệu, màu, nozzle, layer height và số lượng in.

## 14. Các câu hỏi còn mở trước khi bắt đầu CAD

1. “Hình trụ giống Sonos One” có đúng là **trụ tiết diện rounded-square** hay cần trụ tròn tuyệt đối?
2. Kích thước ngoài 135 × 135 × 224 có được chấp nhận, hay có giới hạn kích thước cụ thể?
3. Top cap có được phép dùng liên kết nội bộ/ẩn, hay phải tháo độc lập từ bên ngoài?
4. Cần đo OD, chiều dài và hình dạng lỗ đề xuất của insert M3 và M2 đang có; đồng thời xác nhận kiểu đầu vít M3 × 16 và M2 × 10.
5. Mặt dưới có cần lỗ dây, bass port, tripod, tem hoặc QR/serial không?
6. Pattern lỗ cần quấn 360° hay chỉ mặt trước và hai bên?
7. PETG Bambu Lab đang dùng là dòng cụ thể nào và màu nào cho thân xám/cap cam (ví dụ mã sản phẩm trên spool)?
8. Màu và độ bóng mục tiêu: xám nhám/cam nhám hay bề mặt khác?
9. Có yêu cầu chống bụi, chống nước hoặc lưới vải phía trong sleeve không?
10. Có cần giữ nguyên hoàn toàn chiều cao 196.5 của baseline ở mặt ngoài, hay được tăng thành 224 như concept draft?

---

### Quy tắc bắt đầu dựng thật

Chỉ bắt đầu sửa/dựng Fusion sau khi các mục trong phần 1 và phần 14 được chỉnh hoặc xác nhận. File nguồn V6 phải được giữ nguyên; concept mới được tạo thành design/revision riêng.
