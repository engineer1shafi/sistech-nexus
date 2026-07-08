import { useState } from "react";
import { Loader } from "lucide-react";
import { pollDevice } from "../../services/deviceApi";

type Props = {
  deviceId: string;
  onSuccess?: () => void;
};

export default function PollButton({ deviceId, onSuccess }: Props) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handlePoll = async () => {
    setLoading(true);
    setMessage(null);
    try {
      await pollDevice(deviceId);
      setMessage("Poll successful");
      onSuccess && onSuccess();
    } catch (err: any) {
      setMessage(err?.response?.data?.detail ?? err?.message ?? "Poll failed");
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(null), 4000);
    }
  };

  return (
    <div>
      <button
        onClick={handlePoll}
        disabled={loading}
        className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 px-4 py-2 rounded-xl font-semibold"
      >
        {loading ? <Loader className="animate-spin" size={16} /> : "Poll Now"}
      </button>

      {message && <div className="mt-2 text-sm text-slate-300">{message}</div>}
    </div>
  );
}
