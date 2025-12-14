"use client";

import Link from "next/link";
import { useAuth } from "../contexts/AuthContext";
import SignoutButton from "./SignoutButton";

const Navbar = () => {
  const { user } = useAuth();

  return (
    <nav className="flex items-center justify-between px-6 py-3 bg-white shadow-lg transition-all duration-300 ease-in-out">
      <div className="text-2xl font-extrabold text-indigo-700 tracking-wide">
        <Link href="/" className="hover:text-indigo-900 transition-colors duration-200">Todo App</Link>
      </div>
      <div>
        {user ? (
          <div className="flex items-center space-x-4">
            <span className="text-gray-700 font-medium">Welcome, {user.email}</span>
            <SignoutButton />
          </div>
        ) : (
          <div className="space-x-4">
            <Link href="/signin" className="px-5 py-2 font-semibold text-white bg-indigo-600 rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-75 transition-all duration-300 ease-in-out">
              Sign In
            </Link>
            <Link href="/signup" className="px-5 py-2 font-semibold text-indigo-700 bg-indigo-100 rounded-lg shadow-md hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-75 transition-all duration-300 ease-in-out">
              Sign Up
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
