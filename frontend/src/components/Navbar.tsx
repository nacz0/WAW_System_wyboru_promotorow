import React from "react";
import {
  Navbar as NextUINavbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  NavbarMenuToggle,
  NavbarMenu,
  NavbarMenuItem,
  Link,
  Button,
} from "@nextui-org/react";
import { GraduationCap, Menu, X } from "lucide-react";
import { Link as RouterLink, useLocation } from "react-router-dom";

export const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);
  const location = useLocation();

  const menuItems = [
    { name: "Główna", path: "/" },
    { name: "Promotorzy", path: "/promotorzy" },
    { name: "Moje Wybory", path: "/moje-wybory" },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <NextUINavbar 
      onMenuOpenChange={setIsMenuOpen} 
      isBordered 
      maxWidth="xl" 
      className="backdrop-blur-md bg-white/70"
    >
      <NavbarContent>
        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Zamknij menu" : "Otwórz menu"}
          className="sm:hidden"
        />
        <NavbarBrand>
          <RouterLink to="/" className="flex items-center gap-2 group">
            <div className="bg-primary p-2 rounded-xl text-white group-hover:rotate-12 transition-transform duration-300">
              <GraduationCap size={24} />
            </div>
            <p className="font-black text-inherit text-xl hidden sm:block tracking-tighter">
              SYSTEM SELEKCJI
            </p>
          </RouterLink>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="hidden sm:flex gap-8" justify="center">
        {menuItems.map((item) => (
          <NavbarItem key={item.path} isActive={isActive(item.path)}>
            <Link 
              as={RouterLink} 
              color={isActive(item.path) ? "primary" : "foreground"} 
              to={item.path}
              className={`text-sm font-bold uppercase tracking-wider transition-all hover:opacity-100 ${isActive(item.path) ? 'scale-110' : 'opacity-60'}`}
            >
              {item.name}
            </Link>
          </NavbarItem>
        ))}
      </NavbarContent>

      <NavbarContent justify="end">
        <NavbarItem className="hidden sm:flex">
          <Button as={RouterLink} to="/login" variant="light" className="font-bold">
            Zaloguj
          </Button>
        </NavbarItem>
        <NavbarItem>
          <Button 
            as={RouterLink} 
            color="primary" 
            to="/rejestracja" 
            variant="shadow" 
            className="font-bold px-6 bg-gradient-to-tr from-blue-600 to-indigo-500"
          >
            Start
          </Button>
        </NavbarItem>
      </NavbarContent>

      {/* Menu mobilne */}
      <NavbarMenu className="bg-white/90 backdrop-blur-3xl pt-8 gap-6">
        {menuItems.map((item, index) => (
          <NavbarMenuItem key={`${item.name}-${index}`}>
            <Link
              as={RouterLink}
              color={isActive(item.path) ? "primary" : "foreground"}
              className="w-full text-2xl font-black py-4"
              to={item.path}
              size="lg"
              onClick={() => setIsMenuOpen(false)}
            >
              {item.name}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </NextUINavbar>
  );
};
