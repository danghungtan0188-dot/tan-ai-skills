import React from "react";
import { Composition } from "remotion";
import { FPS, metadata } from "./chung";
import { AnhKet, anhKetSchema } from "./mau/AnhKet";
import { AnhTuLieu, anhTuLieuSchema } from "./mau/AnhTuLieu";
import { BanDoXa, banDoXaSchema } from "./mau/BanDoXa";
import { BannerPhongSu, bannerPhongSuSchema } from "./mau/BannerPhongSu";
import { GiamNgheo, giamNgheoSchema } from "./mau/GiamNgheo";
import { HaoGiaoThong, haoGiaoThongSchema } from "./mau/HaoGiaoThong";
import { HaTang, haTangSchema } from "./mau/HaTang";
import { HopThongTin, hopThongTinSchema } from "./mau/HopThongTin";
import { MocThoiGian, mocThoiGianSchema } from "./mau/MocThoiGian";
import { ChuDong, chuDongSchema } from "./mau/ChuDong";
import { Intro, introSchema } from "./mau/Intro";
import { LowerThird, lowerThirdSchema } from "./mau/LowerThird";
import { SoLieu, soLieuSchema } from "./mau/SoLieu";
import { SoLieuTran, soLieuTranSchema } from "./mau/SoLieuTran";
import { TheKet, theKetSchema } from "./mau/TheKet";
import { TieuChi, tieuChiSchema } from "./mau/TieuChi";
import { TieuDeLon, tieuDeLonSchema } from "./mau/TieuDeLon";
import { TriAn, triAnSchema } from "./mau/TriAn";
import { TuyenVanChuyen, tuyenVanChuyenSchema } from "./mau/TuyenVanChuyen";
import { VetSang, vetSangSchema } from "./mau/VetSang";
import { TranhGiay, tranhGiaySchema } from "./mau/TranhGiay";
import { TranhGiayPhuNu, tranhGiayPhuNuSchema } from "./mau/TranhGiayPhuNu";
import { PhuNu96, phuNu96Schema } from "./mau/PhuNu96";
import { KetLaser, ketLaserSchema } from "./mau/KetLaser";
import { BanDoVeTinh, banDoVeTinhSchema } from "./mau/BanDoVeTinh";
import { SoLan, soLanSchema } from "./mau/SoLan";
import { HudDemSo, hudDemSoSchema } from "./mau/HudDemSo";
import { AnhBayVao, anhBayVaoSchema } from "./mau/AnhBayVao";
import { NguoiNoiPip, nguoiNoiPipSchema } from "./mau/NguoiNoiPip";
import { TieuDeNhan, tieuDeNhanSchema } from "./mau/TieuDeNhan";

// Kích thước/thời lượng thật tính trong calculateMetadata từ props `tiLe` + `thoiLuong`.
const chung = { fps: FPS, width: 1920, height: 1080, durationInFrames: 120 } as const;

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="HaTang"
      component={HaTang}
      schema={haTangSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 5, tieuDe: "", nenMo: true, muc: [{ loai: "giao_thong", nhan: "Giao thông", tai: 0.5 }] }}
      {...chung}
    />
    <Composition
      id="GiamNgheo"
      component={GiamNgheo}
      schema={giamNgheoSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{
        tiLe: "16:9", thoiLuong: 8, tieuDe: "Tỷ lệ hộ nghèo", truoc: { so: 40, nhan: "Sau chiến tranh", tienTo: "~", soLe: 0 },
        nay: { so: 0.58, nhan: "Hiện nay", tienTo: "", soLe: 2 }, taiTruoc: 0.5, taiNay: 3, nenMo: true,
      }}
      {...chung}
    />
    <Composition
      id="TieuChi"
      component={TieuChi}
      schema={tieuChiSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{
        tiLe: "16:9", thoiLuong: 10, tieuDe: "", so: 5, dat: [2, 4, 5], taiHien: 0.5, taiDat: [2, 3, 4],
        dongDat: "", taiHoiTu: 6, ketLuan: "Mẫu", taiKet: 7, kieu: "tram",
      }}
      {...chung}
    />
    <Composition
      id="MocThoiGian"
      component={MocThoiGian}
      schema={mocThoiGianSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 6, moc: [{ nam: "1940", nhan: "Mẫu", tai: 0.5 }, { nam: "1945", nhan: "Mẫu", tai: 3 }] }}
      {...chung}
    />
    <Composition
      id="HaoGiaoThong"
      component={HaoGiaoThong}
      schema={haoGiaoThongSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{
        tiLe: "16:9",
        thoiLuong: 6,
        tieuDe: "",
        tuyen: [{ ten: "Tuyến 1", diem: [[300, 500], [1500, 400]], tai: 0.5, lau: 2 }],
        km: { so: 4, tienTo: "gần ", tai: 1, lau: 2 },
      }}
      {...chung}
    />
    <Composition
      id="AnhKet"
      component={AnhKet}
      schema={anhKetSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 6, anh: "anh.png", tamX: 50, tamY: 40, zoom: 0.1, taiSang: 1.5 }}
      {...chung}
    />
    <Composition
      id="TriAn"
      component={TriAn}
      schema={triAnSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 8, muc: [{ so: "100", nhan: "mẫu", tai: 1 }], loiDe: "", taiLoiDe: 0 }}
      {...chung}
    />
    <Composition
      id="SoLieuTran"
      component={SoLieuTran}
      schema={soLieuTranSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 5, tieuDe: "", nenMo: true, muc: [{ so: 100, nhan: "mẫu", tai: 0.3, tienTo: "", soLe: 0, donVi: "" }] }}
      {...chung}
    />
    <Composition
      id="TuyenVanChuyen"
      component={TuyenVanChuyen}
      schema={tuyenVanChuyenSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{
        tiLe: "16:9",
        thoiLuong: 6,
        tieuDe: "",
        diem: [
          { ten: "A", x: 1400, y: 800, tai: 0.5, canhTrai: false },
          { ten: "B", x: 500, y: 300, tai: 3, canhTrai: false },
        ],
      }}
      {...chung}
    />
    <Composition
      id="AnhTuLieu"
      component={AnhTuLieu}
      schema={anhTuLieuSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 6, anh: "anh.png", chuThich: "", chuThichPhu: "", nghieng: -2, dichLen: 0 }}
      {...chung}
    />
    <Composition
      id="HopThongTin"
      component={HopThongTin}
      schema={hopThongTinSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 4, dongNghieng: "Đầu năm 1940", dong: ["Chi bộ Đảng đầu tiên", "6 đảng viên"], cachDay: 70 }}
      {...chung}
    />
    <Composition
      id="BannerPhongSu"
      component={BannerPhongSu}
      schema={bannerPhongSuSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{
        tiLe: "16:9",
        thoiLuong: 5,
        ten: "Bà NGUYỄN THỊ A",
        diaChi: "Xã An Thạnh Thủy, tỉnh Đồng Tháp",
        nhan: "PHÓNG SỰ",
        mauDam: "#169A4D",
        mauHuyHieu: "#0BA44D",
        mauNhat: "#CBDBBE",
        dichLen: 0,
      }}
      {...chung}
    />
    <Composition
      id="VetSang"
      component={VetSang}
      schema={vetSangSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 0.9, goc: -32 }}
      {...chung}
    />
    <Composition
      id="TieuDeLon"
      component={TieuDeLon}
      schema={tieuDeLonSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 3, chu: "XÃ AN THẠNH THỦY", co: 150, phu: "", nenSang: false }}
      {...chung}
    />
    <Composition
      id="TheKet"
      component={TheKet}
      schema={theKetSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 4, dong1: "An Thạnh Thủy", dong2: "Vùng đất an toàn khu", chiChu: false, treChu: 0 }}
      {...chung}
    />
    <Composition
      id="BanDoXa"
      component={BanDoXa}
      schema={banDoXaSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{
        tiLe: "16:9",
        thoiLuong: 4,
        anhDinhVi: "",
        nhanDinhVi: [],
        ghim: [0.5, 0.5],
        chuyenCanh: 0,
        khung: [0, 0, 160, 90],
        ranhGioi: [[40, 20], [120, 25], [110, 70], [50, 65]],
        duongChia: [],
        veVien: [0.3, 1.2],
        nhan: [{ chu: "X. Mẫu", x: 80, y: 48, tai: 1.5 }],
      }}
      {...chung}
    />
    <Composition
      id="Intro"
      component={Intro}
      schema={introSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{
        tiLe: "16:9",
        thoiLuong: 4,
        tieuDe: "An Thạnh Thủy tập huấn\nsản xuất nông sản an toàn",
        phuDe: "Bản tin xã An Thạnh Thủy",
        ngay: "03/10/2026",
      }}
      {...chung}
    />
    <Composition
      id="SoLieu"
      component={SoLieu}
      schema={soLieuSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{
        tiLe: "16:9",
        thoiLuong: 5,
        tieuDe: "Sản lượng lúa vụ Hè Thu",
        giaTri: 30,
        soLe: 0,
        tienTo: "+",
        donVi: "%",
        moTa: "so với cùng kỳ năm 2025",
        cot: [
          { nhan: "2024", giaTri: 4200 },
          { nhan: "2025", giaTri: 4650 },
          { nhan: "2026", giaTri: 6045 },
        ],
      }}
      {...chung}
    />
    <Composition
      id="LowerThird"
      component={LowerThird}
      schema={lowerThirdSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 5, ten: "Ông Nguyễn Văn A", chucVu: "Chủ tịch UBND xã An Thạnh Thủy" }}
      {...chung}
    />
    <Composition
      id="ChuDong"
      component={ChuDong}
      schema={chuDongSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{
        tiLe: "9:16",
        thoiLuong: 6,
        amThanh: "",
        tieuDe: "Tin nhanh",
        cau: [
          { chu: "Sáng nay, xã An Thạnh Thủy tổ chức tập huấn", start: 0.3, end: 3 },
          { chu: "cho hơn một trăm hộ dân.", start: 3.2, end: 5.6 },
        ],
      }}
      {...chung}
    />
    <Composition
      id="TranhGiay"
      component={TranhGiay}
      schema={tranhGiaySchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 6, dongTren: "Ủy ban nhân dân", dongChinh: "Xã An Thạnh Thủy", dongDuoi: "Đêm hội trăng rằm 2026", moCua: true }}
      {...chung}
    />
    <Composition
      id="TranhGiayPhuNu"
      component={TranhGiayPhuNu}
      schema={tranhGiayPhuNuSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{
        tiLe: "16:9",
        thoiLuong: 14,
        tieuDe: "KỶ NIỆM 96 NĂM",
        dongTen: "Ngày thành lập Hội Liên hiệp Phụ nữ Việt Nam",
        dongNgay: "20/10/1930 – 20/10/2026",
        loiChuc1: "Chúc mừng các bà, các mẹ, các chị em phụ nữ",
        loiChuc2: "Mạnh khỏe · Hạnh phúc · Thành công",
        dongKy: "",
      }}
      {...chung}
    />
    <Composition
      id="SoLan"
      component={SoLan}
      schema={soLanSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 3, tu: "2025", den: "2026", tai: 0.6, tieuDe: "" }}
      {...chung}
    />
    <Composition
      id="HudDemSo"
      component={HudDemSo}
      schema={hudDemSoSchema}
      calculateMetadata={metadata(true)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 5, tu: 0, den: 100, tai: 0.3, denLuc: 4, voO: true, mau: "#FFFFFF" }}
      {...chung}
    />
    <Composition
      id="BanDoVeTinh"
      component={BanDoVeTinh}
      schema={banDoVeTinhSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{
        tiLe: "9:16", thoiLuong: 4, font: "", nen: { file: "nen.jpg", w: 1000, h: 1000, mPx: 4.7 }, can: null,
        tieuDe: { nho: "GÓC NHÌN BẢN ĐỒ", lon: "TÊN TUYẾN", phu: "" }, nguon: [],
        xa: { ten: "", vong: [[0, 0], [1, 0], [1, 1], [0, 0]], nhan: [0, 0] }, kenh: { ten: "", duong: [[0, 0], [1, 1]], nhan: [0, 0] },
        langGieng: [], tuyen: [], cau: null, so: null, canh: [{ tu: 0, cx: 500, cy: 500, zoom: 1 }],
        moc: { kenh: 0, xa: 0, so: 99, tuyen: 99, cau: 99, het: 4 }, cau_doc: [],
      }}
      {...chung}
    />
    <Composition
      id="KetLaser"
      component={KetLaser}
      schema={ketLaserSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 4, font: "", donVi: "Trung tâm Cung ứng dịch vụ công xã An Thạnh Thủy", loiMoi: "Theo dõi ATT NEWS để nhận bản tin của xã mỗi ngày", qrTrai: "", qrPhai: "" }}
      {...chung}
    />
    <Composition
      id="PhuNu96"
      component={PhuNu96}
      schema={phuNu96Schema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 20, intro: "", introDai: 6, font: "", canh: [], ketTren: "Chúc mừng", ketLon: "20/10", ketDuoi: "", ketDau: 0 }}
      {...chung}
    />
    <Composition
      id="AnhBayVao"
      component={AnhBayVao}
      schema={anhBayVaoSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 7, anh: ["anh1.jpg", "anh2.jpg", "anh3.jpg", "anh4.jpg"], cachNhau: 0.45, tieuDe: "" }}
      {...chung}
    />
    <Composition
      id="NguoiNoiPip"
      component={NguoiNoiPip}
      schema={nguoiNoiPipSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 8, video: "nguoi_noi.mp4", doHoa: [{ tu: 2, den: 5.5, file: "anh1.jpg" }], coTron: 220 }}
      {...chung}
    />
    <Composition
      id="TieuDeNhan"
      component={TieuDeNhan}
      schema={tieuDeNhanSchema}
      calculateMetadata={metadata(false)}
      defaultProps={{ tiLe: "16:9", thoiLuong: 4, chu: "Mỗi ngày", nhan: "một bước nhỏ", phu: "" }}
      {...chung}
    />
  </>
);
