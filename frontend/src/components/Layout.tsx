import React from "react";
import { Navbar } from "./Navbar";
import { motion } from "framer-motion";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-slate-50 overflow-x-hidden">
      <Navbar />
      <motion.main
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="container mx-auto max-w-7xl pt-12 px-6 flex-grow"
      >
        {children}
      </motion.main>
      <footer className="w-full flex items-center justify-center py-12 text-slate-400 text-sm">
        <div className="flex flex-col items-center gap-2">
          <p>© 2026 System Wyboru Promotorów</p>
          <div className="h-1 w-12 bg-primary rounded-full opacity-30" />
        </div>
      </footer>
    </div>
  );
};
