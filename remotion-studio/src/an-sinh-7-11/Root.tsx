import React from "react";
import {Composition} from "remotion";
import {DURATION_S} from "./data";
import {AnSinh711} from "./AnSinh711";
import {KetAnhSang} from "./KetAnhSang";

export const Root: React.FC = () => (
  <>
    <Composition id="AnSinh711" component={AnSinh711} durationInFrames={Math.round(DURATION_S * 30)} fps={30} width={1920} height={1080} />
    <Composition id="KetAnhSang" component={KetAnhSang} durationInFrames={120} fps={30} width={1920} height={1080} />
  </>
);
