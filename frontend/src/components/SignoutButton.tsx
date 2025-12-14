"use client";

import { useAuth } from "../contexts/AuthContext";
import { useRouter } from "next/navigation";

const SignoutButton = () => {
  const { signout } = useAuth();
  const router = useRouter();

  const handleSignout = async () => {
    await signout();
    router.push("/signin");
  };

  return (
    <button
      onClick={handleSignout}
      className="px-5 py-2 font-semibold text-white bg-red-600 rounded-lg shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 focus:ring-opacity-75 transition-all duration-300 ease-in-out transform hover:scale-105"
    >
      Sign Out
    </button>
  );
};

export default SignoutButton;
