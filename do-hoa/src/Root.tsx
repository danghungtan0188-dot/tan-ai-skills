import React from "react";
import { Composition } from "remotion";
import { FPS, metadata } from "./chung";
import { ChuDong, chuDongSchema } from "./mau/ChuDong";
import { Intro, introSchema } from "./mau/Intro";
import { LowerThird, lowerThirdSchema } from "./mau/LowerThird";
import { SoLieu, soLieuSchema } from "./mau/SoLieu";

// Kích thước/thời lượng thật tính trong calculateMetadata từ props `tiLe` + `thoiLuong`.
const chung = { fps: FPS, width: 1920, height: 1080, durationInFrames: 120 } as const;

export const RemotionRoot: React.FC = () => (
  <>
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
