// Nội dung + mốc thời gian (giây) theo giọng Tân bản mới (timeline5.json); scenes = màn hình điện thoại vẽ lại
import type {Scene} from "./PhoneMock";

export type Page = {
  step: number;
  from: number;
  to: number;
  title: string;
  items: [string, number][];
  scenes: Scene[];
};

export const DURATION_S = 98.816;
export const OUTRO_FROM = 93.45;

export const STEP_LABELS = ["Cài đặt VNeID", "Tài khoản mức 2", "Đăng nhập", "Tích hợp thẻ BHYT", "Kích hoạt Sổ sức khỏe"];

export const PAGES: Page[] = [
  {
    step: 1, from: 5.95, to: 22.05, title: "Cài đặt hoặc cập nhật ứng dụng VNeID", scenes: [{kind: "store", at: 5.95, typeAt: 16.2, tapAt: 19.5, gpAt: 11.9, asAt: 14.2}],
    items: [
      ["Người dân sử dụng **điện thoại thông minh**", 9.6],
      ["Truy cập **Google Play** (Android) hoặc **App Store** (iPhone)", 11.7],
      ["Tìm ứng dụng **“VNeID”** do Bộ Công an phát hành, tải mới hoặc cập nhật phiên bản mới nhất", 16.2],
    ],
  },
  {
    step: 2, from: 22.05, to: 35.85, title: "Đăng ký, kích hoạt tài khoản định danh điện tử mức độ 2", scenes: [{kind: "cards", at: 22.05, header: "Tài khoản định danh mức 2", cards: [{label: "Thẻ căn cước gắn chip còn giá trị", at: 28.5}, {label: "Điện thoại có số thuê bao", at: 32.0}]}],
    items: [
      ["Khi đi đăng ký, cần chuẩn bị:", 26.2],
      ["**Thẻ căn cước** hoặc căn cước công dân gắn chip còn giá trị", 28.5],
      ["**Điện thoại** có số thuê bao đang sử dụng", 32.0],
    ],
  },
  {
    step: 3, from: 35.85, to: 49.55, title: "Đăng nhập ứng dụng VNeID", scenes: [{kind: "login", at: 35.85, fillAt: 42.6, tapAt: 46.2, okAt: 47.2}],
    items: [
      ["Mở ứng dụng **VNeID**", 41.1],
      ["Nhập **số định danh cá nhân** và **mật khẩu**", 42.8],
      ["Xác thực đăng nhập theo hướng dẫn trên ứng dụng", 45.3],
    ],
  },
  {
    step: 4, from: 49.55, to: 66.0, title: "Tích hợp thẻ bảo hiểm y tế", scenes: [
      {kind: "list", at: 49.55, header: "Trang chủ", rows: [{label: "Ví giấy tờ", tapAt: 58.6}, {label: "Hồ sơ sức khỏe"}, {label: "Dịch vụ khác"}]},
      {kind: "list", at: 59.2, header: "Ví giấy tờ", rows: [{label: "Tích hợp thông tin", tapAt: 60.4}, {label: "Giấy tờ đã tích hợp"}]},
      {kind: "list", at: 61.0, header: "Tích hợp thông tin", rows: [{label: "Tạo mới yêu cầu", tapAt: 61.9}, {label: "Lịch sử yêu cầu"}]},
      {kind: "list", at: 62.5, header: "Chọn loại thông tin", rows: [{label: "Đăng ký xe"}, {label: "Giấy phép lái xe"}, {label: "Thẻ BHYT", tapAt: 63.6}]},
    ],
    items: [
      ["Nếu thẻ BHYT chưa hiển thị, tại giao diện chính:", 52.0],
      ["Chọn **“Ví giấy tờ”** → **“Tích hợp thông tin”**", 58.6],
      ["Chọn **“Tạo mới yêu cầu”** → **“Thẻ BHYT”**", 61.6],
    ],
  },
  {
    step: 4, from: 66.0, to: 78.75, title: "Tích hợp thẻ bảo hiểm y tế", scenes: [
      {kind: "form", at: 66.0, fillAt: 66.4, numAt: 68.0, checkAt: 69.4, tapAt: 70.2, okAt: 70.8},
      {kind: "done", at: 71.8, header: "Ví giấy tờ", title: "Thẻ BHYT điện tử", lines: ["Đã tích hợp", "Dùng khi khám, chữa bệnh"]},
    ],
    items: [
      ["Nhập **đơn vị cấp thẻ, số thẻ BHYT**; xác nhận và gửi yêu cầu", 66.1],
      ["Sau khi xác thực, dùng **thông tin BHYT điện tử** khi khám, chữa bệnh", 71.8],
    ],
  },
  {
    step: 5, from: 78.75, to: 93.45, title: "Kích hoạt Sổ sức khỏe điện tử", scenes: [
      {kind: "list", at: 78.75, header: "Trang chủ", rows: [{label: "Ví giấy tờ"}, {label: "Hồ sơ sức khỏe", tapAt: 82.2}, {label: "Dịch vụ khác"}]},
      {kind: "list", at: 82.8, header: "Hồ sơ sức khỏe", rows: [{label: "Sổ sức khỏe điện tử", tapAt: 84.6}, {label: "Thông tin sức khỏe"}]},
      {kind: "list", at: 85.2, header: "Điều khoản sử dụng", rows: [{label: "Tôi đã đọc và đồng ý", sub: "Xác nhận đồng ý điều khoản", tapAt: 87.6}]},
      {kind: "passcode", at: 88.6, fillAt: 89.2, okAt: 91.2},
    ],
    items: [
      ["Tại màn hình chính, chọn **“Hồ sơ sức khỏe”** → **“Sổ sức khỏe điện tử”**", 81.4],
      ["Đọc điều khoản sử dụng, **xác nhận đồng ý**", 85.6],
      ["Nhập **passcode** của VNeID khi được yêu cầu", 88.9],
    ],
  },
];
