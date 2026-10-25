import {Audio, Video} from "@remotion/media";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type {AttNewsProps} from "./types";

const CaptionLayer: React.FC<Pick<AttNewsProps, "captions">> = ({captions}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const nowMs = (frame / fps) * 1000;
  const cue = captions.find((item) => nowMs >= item.startMs && nowMs < item.endMs);

  if (!cue) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        left: "8%",
        right: "8%",
        bottom: "9%",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          maxWidth: "88%",
          padding: "14px 24px",
          borderRadius: 12,
          backgroundColor: "rgba(3, 16, 38, 0.82)",
          color: "white",
          fontSize: 42,
          fontWeight: 700,
          lineHeight: 1.25,
          textAlign: "center",
          textShadow: "0 2px 5px rgba(0,0,0,0.9)",
        }}
      >
        {cue.text}
      </div>
    </div>
  );
};

export const AttNews: React.FC<AttNewsProps> = (props) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titleOpacity = interpolate(frame, [0, 0.55 * fps], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const titleTranslate = interpolate(frame, [0, 0.7 * fps], ["0px 34px", "0px 0px"], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  return (
    <AbsoluteFill style={{backgroundColor: props.backgroundColor, fontFamily: "Arial, sans-serif"}}>
      {props.backgroundVideo ? (
        <Video
          src={staticFile(props.backgroundVideo)}
          muted
          objectFit="cover"
          style={{width: "100%", height: "100%"}}
        />
      ) : null}
      {props.backgroundImage ? (
        <Img
          src={staticFile(props.backgroundImage)}
          style={{width: "100%", height: "100%", objectFit: "cover"}}
        />
      ) : null}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(90deg, rgba(2,18,48,0.94) 0%, rgba(2,18,48,0.68) 46%, rgba(2,18,48,0.16) 100%)",
        }}
      />

      <div
        style={{
          position: "absolute",
          top: 52,
          left: 64,
          padding: "10px 18px",
          backgroundColor: props.accentColor,
          color: "white",
          fontSize: 28,
          fontWeight: 900,
          letterSpacing: 1.4,
        }}
      >
        ATT NEWS
      </div>

      <div
        style={{
          position: "absolute",
          left: "7%",
          top: "27%",
          width: "63%",
          opacity: titleOpacity,
          translate: titleTranslate,
        }}
      >
        <div style={{color: props.accentColor, fontSize: 30, fontWeight: 800, marginBottom: 18}}>
          {props.kicker}
        </div>
        <div style={{color: "white", fontSize: 76, fontWeight: 900, lineHeight: 1.05}}>
          {props.title}
        </div>
        <div style={{color: "#d8e8ff", fontSize: 34, lineHeight: 1.35, marginTop: 24}}>
          {props.subtitle}
        </div>
      </div>

      <CaptionLayer captions={props.captions} />
      {props.voiceover ? <Audio src={staticFile(props.voiceover)} /> : null}
    </AbsoluteFill>
  );
};
