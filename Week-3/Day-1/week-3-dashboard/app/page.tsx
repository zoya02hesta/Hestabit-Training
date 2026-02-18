import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center space-y-6">
      <h1 className="text-4xl font-bold">
        Welcome to Purity Dashboard
      </h1>

      <div className="space-x-4">
        <Link
          href="/about"
          className="px-6 py-3 bg-gray-800 text-white rounded-xl"
        >
          About
        </Link>

        <Link
          href="/dashboard"
          className="px-6 py-3 bg-blue-600 text-white rounded-xl"
        >
          Go to Dashboard
        </Link>
      </div>
    </div>
  );
}
