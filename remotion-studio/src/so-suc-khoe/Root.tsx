import React from "react";
import {Composition} from "remotion";
import {DURATION_S} from "./data";
import {SoSucKhoe} from "./SoSucKhoe";

export const Root: React.FC = () => (
  <Composition id="SoSucKhoe" component={SoSucKhoe} durationInFrames={Math.round(DURATION_S * 30)} fps={30} width={1920} height={1080} />
);
