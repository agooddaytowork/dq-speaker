# SPEC — SONOS case rectangular compact variant

**Trạng thái:** CAD review clone  
**Phiên bản:** RECT 1.4  
**Baseline:** `SONOS_CASE_CONCEPT_V1`, spec V1.9

Tài liệu này chỉ ghi các override của bản chữ nhật. Mọi mounting geometry, fastener, vật liệu, màu, chiều cao, port, logo, frame, fillet và fit-test requirement không nêu dưới đây giữ nguyên theo [spec.md](./spec.md).

## Kích thước và hình dáng

| Hạng mục | Bản vuông | Bản chữ nhật |
|---|---:|---:|
| Kích thước cap ngoài | 135 × 135 mm | **135 × 99 mm** |
| Sleeve ngoài | 133 × 133 mm | **133 × 97 mm** |
| Chiều cao tổng | 224 mm | **224 mm** |
| Corner radius cap | R28 | **R8** |
| Corner radius sleeve | R27 | **R7** |
| Sleeve wall | 2.0 mm | **2.0 mm** |
| Clearance tới frame theo Y | khoảng 20.5 mm mỗi bên | **2.5 mm mỗi bên** |

## Các thay đổi bắt buộc đi kèm

- Groove top/bottom đổi theo sleeve 133 × 97, giữ engagement và clearance cũ.
- Pattern capsule tiếp tục phủ bốn mặt và bốn góc; số lỗ giảm theo diện tích bề mặt mới.
- Logo `DQ` chuyển về thành trước mới tại Y = +48.5 mm; hình dạng và độ nổi giữ nguyên.
- Bốn lỗ M3 top/bottom và bốn screw plug giữ nguyên tọa độ X = ±45, Y = ±35.
- Bốn chân Ø10 của baseline `Extrude1` (Z = -4.2 đến +0.8) được giữ nguyên chức năng và chuyển tới X = ±55, Y = ±28 để nằm trong đáy mới, tránh counterbore M3.
- Frame V1.9 giữ nguyên hoàn toàn, gồm front columns Ø4.2 và cặp cạnh đỏ dịch tới Z = 58.25 mm.

## Top cap — service pocket cho USB-C và power

- Khoét âm từ mặt trong top cap sâu **8.0 mm**, dừng tại Z = 220 mm.
- Giữ lại top skin dày **4.0 mm** tại phần mặt trên.
- Không cắt vào groove kết nối outer sleeve; giữa biên pocket và mép trong groove giữ wall danh nghĩa **2.5 mm**.
- Giữ bốn island R9 quanh lỗ M3 để bảo toàn vai đỡ đầu vít và độ cứng cục bộ.
- Hai lỗ Ø11 USB-C và Ø13 power xuyên tới mặt đáy pocket mới, tạo không gian thao tác và mặt tựa cho retaining nut.

## Tay cầm bắt xuyên bốn vít M3

- Thêm một component tay cầm PETG màu cam, tháo rời được.
- Dùng lại đúng bốn tâm vít của top cap: X = ±45 mm, Y = ±35 mm.
- Chuỗi lắp: đầu vít M3 → tay cầm → top cap → insert trên front/rear frame.
- Phần chân đổi thành hai cụm chữ V đối xứng, arm rộng 8 mm: hàng vít Y = -35 hội tụ về support tại (0, -25), hàng vít Y = +35 hội tụ về support tại (0, +25).
- Grip Ø14 đặt chính giữa X = 0, chạy trước–sau từ Y = -35 đến +35 tại Z = 260 mm; hai support Ø14 và các đầu grip dùng chuyển tiếp cầu bo tròn.
- Không còn rail chạy cạnh lỗ power. USB-C và power nằm trong vùng trống giữa các arm chữ V để thao tác trực tiếp từ mặt trên.
- Toàn bộ cạnh ngoài của V-base, arm và mounting pad dùng Fusion Fillet feature R1.5.
- Bốn phía chân support dùng một Fusion Fillet feature R2; V-base R1.5 bật tangent-chain để bo liên tục qua các đoạn cạnh bị chia tại nút hội tụ.
- Miệng counterbore đầu vít bo R0.6; mép dẫn locator và đầu ra lỗ M3 bo R0.3.
- Các mặt tựa đầu vít tại Z = 223.8 và vai locator giữ phẳng/sắc để bảo toàn lực kẹp và kích thước lắp.
- Mỗi chân có locator Ø8.9 ăn vào screw-plug pocket Ø9.2 có sẵn.
- Dùng **M3×20** cho bốn vị trí tay cầm. Đầu vít nằm trong counterbore Ø6.3, mặt tựa tại Z = 223.8 mm; đầu vít tới khoảng Z = 203.8 mm và xuyên hết chiều dài insert Z = 204.5–212 mm.
- Không dùng M3×30 tại bốn vị trí này vì chiều dài dư có thể đi quá đáy boss/insert.
- Khi lắp tay cầm, tháo và không dùng bốn screw plug; screw plug vẫn được giữ trong file như cấu hình tùy chọn.

## Điều kiện đạt review

- Sleeve, top cap và bottom cap là mỗi component một solid liên tục.
- Top cap còn top skin 4.0 mm; groove sleeve và bốn bệ M3 không bị pocket cắt mất.
- Tay cầm là một solid; không interference với top cap, sleeve, frame hoặc hai port trong cấu hình lắp tay cầm.
- Không interference giữa 9 body in.
- Lòng sleeve không cấn frame; khoảng hở danh nghĩa nhỏ nhất theo Y là 2.5 mm mỗi bên.
- Tất cả part vẫn nằm trong build volume 250 × 250 × 250 mm.
