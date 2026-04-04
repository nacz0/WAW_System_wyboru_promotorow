import React, { useState, useEffect } from "react";
import { 
  Input, 
  Button, 
  Card, 
  CardBody, 
  User, 
  Chip, 
  Select, 
  SelectItem,
  Skeleton,
  CardFooter,
  Divider,
  Pagination
} from "@nextui-org/react";
import { Search, Filter, Star, GraduationCap, MapPin, Sparkles, TrendingUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate, Link } from "react-router-dom";

const DUMMY_PROMOTORS = Array.from({ length: 12 }).map((_, i) => ({
  id: i + 1,
  name: i % 2 === 0 ? "prof. dr hab. Jan Kowalski" : "dr inż. Anna Nowak",
  department: i % 3 === 0 ? "Informatyka" : i % 3 === 1 ? "Telekomunikacja" : "Matematyka",
  specialization: i % 4 === 0 ? "Sztuczna Inteligencja" : i % 4 === 1 ? "Cyberbezpieczeństwo" : "Data Science",
  spots: { total: 10, taken: Math.floor(Math.random() * 11) },
  rating: (4 + Math.random()).toFixed(1),
  avatar: `https://i.pravatar.cc/150?u=${i + 20}`,
}));

export const Promotorzy = () => {
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 800);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="flex flex-col gap-10 relative">
      {/* Subtle Background Elements */}
      <div className="absolute top-40 right-[-10%] w-96 h-96 bg-primary/5 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-40 left-[-10%] w-80 h-80 bg-blue-500/5 rounded-full blur-[100px] pointer-events-none" />

      <header className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 relative z-10">
        <motion.div 
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex flex-col gap-2"
        >
          <div className="flex items-center gap-2 mb-2">
             <Chip color="primary" variant="flat" size="sm" className="font-black border-none uppercase tracking-widest text-[9px]">Eksperci Akademiccy</Chip>
             <TrendingUp size={16} className="text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-black tracking-tighter text-slate-900 leading-none mb-2">Wybierz Mistrza.</h1>
          <p className="text-default-500 text-lg max-w-2xl font-medium leading-relaxed">
             Nasza kadra to naukowcy z pasją. Znajdź osobę, której doświadczenie pomoże Ci zrealizować ambitne plany dyplomowe.
          </p>
        </motion.div>
        <motion.div 
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex flex-col items-end gap-1 bg-white p-6 rounded-[2rem] shadow-xl border border-default-100"
        >
           <span className="text-default-400 text-[10px] font-black uppercase tracking-[0.2em]">Wolnych Miejsc</span>
           <span className="text-4xl font-black text-primary tracking-tighter">142</span>
        </motion.div>
      </header>

      {/* Modern Filter Bar with InView animation */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="sticky top-[72px] z-20"
      >
        <Card className="border-none bg-white/80 backdrop-blur-xl shadow-[0_20px_50px_rgba(0,0,0,0.05)] p-2 rounded-[2rem]">
          <CardBody className="flex flex-col lg:flex-row gap-4 p-2 items-center">
            <Input
              placeholder="Wpisz nazwisko, katedrę lub słowo kluczowe..."
              startContent={<Search size={20} className="text-primary" />}
              className="w-full lg:flex-grow"
              size="lg"
              variant="flat"
              classNames={{
                inputWrapper: "bg-default-50 hover:bg-white border-none transition-all rounded-2xl h-14"
              }}
            />
            <div className="flex gap-3 w-full lg:w-auto">
               <Select 
                  placeholder="Katedra" 
                  className="w-full lg:w-56"
                  size="sm"
                  variant="flat"
                  classNames={{ trigger: "h-14 rounded-2xl bg-default-50" }}
                >
                  <SelectItem key="it">Systemy Informatyczne</SelectItem>
                  <SelectItem key="tele">Teleinformatyka</SelectItem>
                  <SelectItem key="math">Matematyka Stosowana</SelectItem>
                </Select>
                <Button color="primary" size="lg" className="h-14 w-14 min-w-[56px] rounded-2xl shadow-xl shadow-primary/20">
                  <Filter size={20} />
                </Button>
            </div>
          </CardBody>
        </Card>
      </motion.div>

      {/* Grid with STAGGERED SCROLL REVEAL */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        <AnimatePresence>
          {isLoading ? (
            Array.from({ length: 8 }).map((_, i) => (
              <Card key={i} className="p-4 gap-4 bg-white/50 border-none shadow-sm rounded-3xl">
                <Skeleton className="rounded-2xl h-12 w-12" />
                <div className="space-y-3">
                  <Skeleton className="h-4 w-3/4 rounded-lg" />
                  <Skeleton className="h-4 w-1/2 rounded-lg" />
                </div>
                <Divider />
                <Skeleton className="h-24 w-full rounded-3xl" />
              </Card>
            ))
          ) : (
            DUMMY_PROMOTORS.map((promotor, idx) => (
              <motion.div
                key={promotor.id}
                initial={{ opacity: 0, y: 60 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ 
                   duration: 0.6, 
                   delay: (idx % 4) * 0.1, // Stagger based on column index
                   ease: "easeOut"
                }}
              >
                <Card 
                  className="group hover:shadow-[0_30px_60px_-15px_rgba(0,0,0,0.1)] transition-all duration-500 border-none bg-white p-2 h-full rounded-[2.5rem] relative overflow-hidden"
                  isPressable
                  onPress={() => navigate(`/profil/${promotor.id}`)}
                >
                  <CardBody className="p-6">
                    <div className="flex justify-between items-start mb-8 relative z-10">
                      <User
                        name={promotor.name}
                        description={promotor.department}
                        avatarProps={{
                          src: promotor.avatar,
                          size: "lg",
                          radius: "full",
                          isBordered: true,
                          color: "primary",
                          className: "transition-transform group-hover:scale-110"
                        }}
                        classNames={{
                          name: "font-black text-lg text-slate-800 tracking-tighter",
                          description: "text-primary font-bold text-[10px] uppercase tracking-widest mt-1"
                        }}
                      />
                      <Chip 
                        startContent={<Star size={10} fill="currentColor" />} 
                        variant="flat" 
                        color="warning" 
                        size="sm"
                        className="font-black bg-warning/10 text-warning"
                      >
                        {promotor.rating}
                      </Chip>
                    </div>
                    
                    <div className="space-y-4 mb-6">
                       <div className="bg-default-50 p-5 rounded-[1.5rem] transition-colors group-hover:bg-primary/5 border border-transparent group-hover:border-primary/10">
                          <p className="text-[10px] uppercase font-black text-default-400 tracking-widest mb-2 flex items-center gap-2">
                             <Sparkles size={12} className="text-primary" /> Ekspertyza
                          </p>
                          <p className="text-sm font-bold text-slate-700 leading-tight">
                             {promotor.specialization} & Systemy Autonomiczne
                          </p>
                       </div>
                    </div>

                    <div className="flex items-center gap-3 px-1 mb-6 text-default-400">
                       <MapPin size={16} />
                       <span className="text-xs font-bold">Wydział Techniczny, Budynek D-2</span>
                    </div>

                    <div className="flex justify-between items-center bg-slate-900 rounded-[2rem] p-4 text-white">
                       <div className="flex flex-col ml-2">
                          <span className="text-2xl font-black leading-none">{Math.max(0, promotor.spots.total - promotor.spots.taken)}</span>
                          <span className="text-[8px] uppercase font-black opacity-50 tracking-widest">Wolnych</span>
                       </div>
                       <Button 
                          color="primary" 
                          variant="shadow"
                          className="font-black rounded-xl px-8 h-12 bg-white text-slate-900 data-[hover=true]:bg-primary data-[hover=true]:text-white transition-colors"
                          size="md"
                        >
                          PROFIL
                        </Button>
                    </div>
                  </CardBody>
                </Card>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>

      <motion.footer 
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        className="flex justify-center pt-12 pb-20"
      >
         <Pagination 
            showControls 
            total={10} 
            color="primary" 
            variant="flat" 
            classNames={{
               cursor: "bg-primary text-white font-black h-14 w-14 rounded-2xl shadow-2xl shadow-primary/30",
               item: "h-14 w-14 rounded-2xl font-black bg-white shadow-sm hover:bg-default-100 transition-colors mx-1"
            }}
          />
      </motion.footer>
    </div>
  );
};
