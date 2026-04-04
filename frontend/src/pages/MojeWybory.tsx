import React from "react";
import {
  Card,
  CardBody,
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  User,
  Chip,
  Button,
  Badge,
  Tooltip,
  Divider,
  Progress
} from "@nextui-org/react";
import { Star, ArrowUpDown, Trash2, Send, GraduationCap, Info, ChevronRight, Activity } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const DUMMY_CHOICES = [
  { id: 1, name: "prof. dr hab. Jan Kowalski", department: "Informatyka", priority: 1, status: "Zatwierdzone", topic: "Analiza szeregów czasowych w medycynie", average: 4.8 },
  { id: 2, name: "dr inż. Anna Nowak", department: "Telekomunikacja", priority: 2, status: "Oczekujące", topic: "Bezpieczeństwo sieci 5G", average: 4.5 },
  { id: 3, name: "dr hab. Mariusz Wilk", department: "Matematyka", priority: 3, status: "Brak miejsc", topic: "Szyfry kwantowe", average: 4.2 },
];

export const MojeWybory = () => {
  return (
    <div className="flex flex-col gap-10 pb-20">
      {/* Header Section */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 bg-white p-8 rounded-3xl shadow-sm">
        <div className="flex flex-col gap-2">
          <Chip color="primary" variant="flat" size="sm" startContent={<Activity size={12} />} className="font-bold border-none">System Aktywny</Chip>
          <h1 className="text-4xl md:text-5xl font-black tracking-tighter text-slate-800">Twoja Lista Wyborów</h1>
          <div className="flex flex-col mt-4">
             <div className="flex justify-between mb-1">
                <span className="text-xs font-bold text-default-400 uppercase">Twoja Średnia: 4.75</span>
                <span className="text-xs font-bold text-primary italic uppercase">TOP 5%</span>
             </div>
             <Progress value={95} color="primary" size="sm" className="max-w-xs" />
          </div>
        </div>
        <div className="flex gap-3 w-full md:w-auto">
           <Button color="primary" size="lg" className="flex-grow md:flex-grow-0 font-bold shadow-xl shadow-primary/20 h-16 rounded-2xl" startContent={<Send size={20} />} variant="shadow">
              Wyślij Listę
           </Button>
        </div>
      </header>

      {/* Desktop View Table */}
      <div className="hidden lg:block">
        <Card className="shadow-xl border-none p-2 bg-white/60 backdrop-blur-md">
          <CardBody className="p-0">
            <Table 
              aria-label="Twoje Wybory" 
              shadow="none" 
              selectionMode="none"
              color="primary"
              classNames={{
                 th: "bg-default-50 py-6 text-default-400 font-black uppercase text-[10px] tracking-widest",
                 td: "py-6 border-b border-default-50/50 last:border-none",
              }}
            >
              <TableHeader>
                <TableColumn>PRIORYTET</TableColumn>
                <TableColumn>PROMOTOR</TableColumn>
                <TableColumn>TEMAT PRACY</TableColumn>
                <TableColumn>STATUS</TableColumn>
                <TableColumn>AKCJE</TableColumn>
              </TableHeader>
              <TableBody>
                {DUMMY_CHOICES.map((choice, idx) => (
                  <TableRow key={choice.id}>
                    <TableCell>
                      <motion.div 
                        whileHover={{ scale: 1.1 }}
                        className="bg-primary/10 w-12 h-12 rounded-2xl flex items-center justify-center font-black text-xl text-primary border border-primary/20"
                      >
                        {choice.priority}
                      </motion.div>
                    </TableCell>
                    <TableCell>
                      <User
                        name={choice.name}
                        description={choice.department}
                        avatarProps={{
                          src: `https://i.pravatar.cc/150?u=${choice.id + 50}`,
                          radius: "xl",
                          color: "primary",
                          isBordered: true,
                          size: "lg"
                        }}
                         classNames={{
                          name: "font-black text-slate-700",
                          description: "text-[10px] uppercase font-bold text-primary"
                        }}
                      />
                    </TableCell>
                    <TableCell>
                       <div className="flex flex-col max-w-[280px] gap-1">
                          <span className="text-sm font-bold text-slate-800 leading-tight">{choice.topic}</span>
                          <span className="text-[10px] text-default-400 uppercase font-black tracking-tight">Kierunek: Inżynieria Danych</span>
                       </div>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        color={choice.status === "Zatwierdzone" ? "success" : choice.status === "Oczekujące" ? "warning" : "danger"} 
                        variant="flat"
                        size="md"
                        className="font-black border-none uppercase px-3"
                      >
                        {choice.status}
                      </Chip>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                         <Tooltip content="Zmień priorytet" color="primary">
                            <Button isIconOnly variant="flat" size="md" className="bg-default-100 hover:bg-primary hover:text-white transition-all rounded-xl">
                               <ArrowUpDown size={18} />
                            </Button>
                         </Tooltip>
                         <Tooltip content="Szczegóły" color="foreground">
                            <Button isIconOnly variant="flat" size="md" className="bg-default-100 rounded-xl">
                               <Info size={18} />
                            </Button>
                         </Tooltip>
                         <Tooltip content="Usuń" color="danger">
                            <Button isIconOnly variant="flat" color="danger" size="md" className="rounded-xl">
                               <Trash2 size={18} />
                            </Button>
                         </Tooltip>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardBody>
        </Card>
      </div>

      {/* Mobile/Tablet View (Cards instead of Table) */}
      <div className="lg:hidden flex flex-col gap-6">
         {DUMMY_CHOICES.map((choice, idx) => (
            <motion.div
               key={choice.id}
               initial={{ opacity: 0, x: -20 }}
               animate={{ opacity: 1, x: 0 }}
               transition={{ delay: idx * 0.1 }}
            >
               <Card className="border-none shadow-lg">
                  <CardBody className="p-6 flex flex-col gap-4">
                     <div className="flex justify-between items-center">
                        <div className="flex items-center gap-3">
                           <div className="bg-primary text-white w-8 h-8 rounded-lg flex items-center justify-center font-black">
                              {choice.priority}
                           </div>
                           <span className="text-xs font-black text-default-400 uppercase tracking-widest">Priorytet</span>
                        </div>
                        <Chip 
                           color={choice.status === "Zatwierdzone" ? "success" : choice.status === "Oczekujące" ? "warning" : "danger"} 
                           variant="flat"
                           size="sm"
                           className="font-black border-none"
                        >
                           {choice.status}
                        </Chip>
                     </div>
                     <Divider className="opacity-50" />
                     <User
                        name={choice.name}
                        description={choice.department}
                        avatarProps={{
                           src: `https://i.pravatar.cc/150?u=${choice.id + 50}`,
                           radius: "lg",
                           color: "primary",
                           isBordered: true,
                           size: "md"
                        }}
                        classNames={{ name: "font-black" }}
                     />
                     <div className="bg-default-50 p-4 rounded-xl">
                        <p className="text-xs text-default-400 font-bold mb-1 uppercase tracking-tighter">Temat wybrany:</p>
                        <p className="text-sm font-semibold text-slate-800">{choice.topic}</p>
                     </div>
                     <div className="flex gap-2 w-full">
                        <Button color="primary" variant="flat" className="flex-grow font-bold rounded-xl" startContent={<ArrowUpDown size={16} />}>Zmień</Button>
                        <Button color="danger" variant="flat" className="font-bold rounded-xl" isIconOnly><Trash2 size={18} /></Button>
                     </div>
                  </CardBody>
               </Card>
            </motion.div>
         ))}
      </div>

      {/* Info Section */}
      <section className="bg-gradient-to-br from-indigo-900 to-blue-900 p-8 md:p-12 rounded-[2.5rem] text-white shadow-2xl relative overflow-hidden">
         <div className="absolute top-0 left-0 w-full h-full opacity-10 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white via-transparent to-transparent pointer-events-none" />
         <div className="max-w-4xl mx-auto flex flex-col lg:flex-row gap-10 items-center relative z-10">
            <div className="bg-white/10 p-8 rounded-[2rem] border border-white/10 backdrop-blur-xl">
               <Star size={48} className="text-warning fill-warning" />
            </div>
            <div className="flex flex-col gap-4 text-center lg:text-left">
               <h3 className="text-3xl font-black tracking-tight">Klucz do sukcesu: Twoja Średnia</h3>
               <p className="text-blue-100 text-lg leading-relaxed opacity-90">
                  W tym systemie priorytet wyboru zależy bezpośrednio od Twoich wyników w nauce. Premiujemy sumienność – studenci z najwyższymi średnimi mają pierwszeństwo w realizacji swoich marzeń naukowych.
               </p>
               <div className="flex flex-wrap gap-4 mt-2 justify-center lg:justify-start">
                  <Button size="lg" className="font-black bg-white text-indigo-900 rounded-2xl px-10">Pobierz Regulamin</Button>
                  <Button size="lg" variant="bordered" className="text-white border-white/20 font-black rounded-2xl hover:bg-white/10 transition-colors">Więcej informacji</Button>
               </div>
            </div>
         </div>
      </section>
    </div>
  );
};
