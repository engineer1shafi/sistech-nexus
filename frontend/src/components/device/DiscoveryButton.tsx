import { useState } from "react";
import { Loader } from "lucide-react";
import { discoverInterfaces } from "../../services/deviceApi";

type Props = {
  deviceId: string;
  onSuccess?: () => void;
};

export default function DiscoveryButton({ deviceId, onSuccess }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDiscover = async () => {
    setLoading(true);
    setError(null);
    try {
      await discoverInterfaces(deviceId);
      onSuccess && onSuccess();
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? err?.message ?? "Discovery failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button
        onClick={handleDiscover}
        disabled={loading}
        className="flex items-center gap-2 bg-cyan-600 hover:bg-cyan-700 disabled:opacity-60 px-4 py-2 rounded-xl font-semibold"
      >
        {loading ? <Loader className="animate-spin" size={16} /> : "Discover Interfaces"}
      </button>

      {error && (
        <div className="mt-2 text-sm text-red-400">{error}</div>
      )}
    </div>
  );
}
