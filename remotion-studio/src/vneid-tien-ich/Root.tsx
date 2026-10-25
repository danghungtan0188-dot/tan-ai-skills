import React from "react";
import {Composition} from "remotion";
import {DURATION_S} from "./data";
import {VneidTienIch} from "./VneidTienIch";

export const Root: React.FC = () => (
  <Composition id="VneidTienIch" component={VneidTienIch} durationInFrames={Math.round(DURATION_S * 30)} fps={30} width={1920} height={1080} />
);
