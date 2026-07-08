type Props = { message?: string };

export default function LoadingState({ message = "Loading..." }: Props) {
  return (
    <div className="text-center py-8 text-slate-500">
      <div className="animate-pulse text-2xl">{message}</div>
    </div>
  );
}
