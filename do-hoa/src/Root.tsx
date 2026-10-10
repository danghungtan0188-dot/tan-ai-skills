import React from "react";
import { Composition } from "remotion";
import { FPS, metadata } from "./chung";
import { AnhKet, anhKetSchema } from "./mau/AnhKet";
import { AnhTuLieu, anhTuLieuSchema } from "./mau/AnhTuLieu";
import { BanDoXa, banDoXaSchema } from "./mau/BanDoXa";
import { BannerPhongSu, bannerPhongSuSchema } from "./mau/BannerPhongSu";
import { HaoGiaoThong, haoGiaoThongSchema } from "./mau/HaoGiaoThong";
import { HopThongTin, hopThongTinSchema } from "./mau/HopThongTin";
import { MocThoiGian, mocThoiGianSchema } from "./mau/MocThoiGian";
import { ChuDong, chuDongSchema } from "./mau/ChuDong";
import { Intro, introSchema } from "./mau/Intro";
import { LowerThird, lowerThirdSchema } from "./mau/LowerThird";
import { SoLieu, soLieuSchema } from "./mau/SoLieu";
import { SoLieuTran, soLieuTranSchema } from "./mau/SoLieuTran";
import { TheKet, theKetSchema } from "./mau/TheKet";
import { TieuDeLon, tieuDeLonSchema } from "./mau/TieuDeLon";
import { TriAn, triAnSchema } from "./mau/TriAn";
import { TuyenVanChuyen, tuyenVanChuyenSchema } from "./mau/TuyenVanChuyen";
import { VetSang, vetSangSchema } from "./mau/VetSang";

// Kích thước/thời lượng thật tính trong calculateMetadata từ props `tiLe` + `thoiLuong`.
const chung = { fps: FPS, width: 1920, height: 1080, durationInFrames: 120 } as const;

export const RemotionRoot: React.FC = () => (
  <>
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
      defaultProps={{ tiLe: "16:9", thoiLuong: 5, tieuDe: "", muc: [{ so: 100, nhan: "mẫu", tai: 0.3, tienTo: "" }] }}
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
      defaultProps={{ tiLe: "16:9", thoiLuong: 3, chu: "XÃ AN THẠNH THỦY", co: 150, phu: "" }}
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
  </>
);
