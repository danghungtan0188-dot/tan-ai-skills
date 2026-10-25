export type CaptionCue = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
};

export type AttNewsProps = {
  title: string;
  subtitle: string;
  kicker: string;
  durationSeconds: number;
  width: number;
  height: number;
  backgroundColor: string;
  accentColor: string;
  backgroundImage: string | null;
  backgroundVideo: string | null;
  voiceover: string | null;
  captions: CaptionCue[];
};
