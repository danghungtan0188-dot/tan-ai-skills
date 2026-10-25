import type {CalculateMetadataFunction} from "remotion";
import {Composition} from "remotion";
import {AttNews} from "./AttNews";
import type {AttNewsProps} from "./types";

export const defaultAttNewsProps: AttNewsProps = {
  title: "Bản tin An Thạnh Thủy",
  subtitle: "Khung Remotion dùng chung cho video ATT NEWS",
  kicker: "TIN MỚI",
  durationSeconds: 8,
  width: 1920,
  height: 1080,
  backgroundColor: "#031a3a",
  accentColor: "#e31b23",
  backgroundImage: null,
  backgroundVideo: null,
  voiceover: null,
  captions: [],
};

const calculateMetadata: CalculateMetadataFunction<AttNewsProps> = ({props}) => {
  const fps = 30;
  return {
    durationInFrames: Math.max(1, Math.round(props.durationSeconds * fps)),
    fps,
    width: props.width,
    height: props.height,
  };
};

export const AttNewsComposition: React.FC = () => {
  return (
    <Composition
      id="AttNews"
      component={AttNews}
      durationInFrames={240}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={defaultAttNewsProps}
      calculateMetadata={calculateMetadata}
    />
  );
};
