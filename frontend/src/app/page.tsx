"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/src/contexts/AuthContext";
import Link from "next/link";

const HomePage = () => {
  const { user, signin, signup, signout } = useAuth(); // Destructure all needed from useAuth
  const router = useRouter();

  useEffect(() => {
    if (user) {
      router.push("/dashboard");
    }
  }, [user, router]);

  if (user) {
    return <div>Redirecting to dashboard...</div>;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md text-center">
        <h1 className="text-4xl font-bold text-gray-900">Welcome to Todo App</h1>
        <p className="mt-4 text-lg text-gray-600">
          Your personal task management solution.
        </p>
        <div className="mt-6 space-y-4">
          <Link
  href="/signin"
  className="block w-full py-3 px-4 text-white bg-[#4F39F6] rounded-md shadow hover:bg-[#432DD7] transition-colors duration-300 font-medium"
>
  Sign In
</Link>

          <Link href="/signup" className="block w-full py-3 px-4 text-blue-600 bg-white border border-blue-600 rounded-md shadow hover:bg-gray-50 font-medium">
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;