import React from "react";
import { useParams, Link as RouterLink } from "react-router-dom";
import {
  Card,
  CardBody,
  Button,
  Chip,
  User,
  Tabs,
  Tab,
  Progress,
  Divider,
  Breadcrumbs,
  BreadcrumbItem
} from "@nextui-org/react";
import { 
  GraduationCap, 
  Mail, 
  MapPin, 
  Star, 
  CheckCircle2, 
  ArrowLeft, 
  Link2, 
  Globe, 
  FileText,
  Calendar,
  MessageSquare
} from "lucide-react";
import { motion } from "framer-motion";

const DUMMY_TOPICS = [
  { id: 1, title: "Zastosowanie sieci neuronowych w analizie tekstu", level: "Inżynierska", status: "Dostępny" },
  { id: 2, title: "Optymalizacja algorytmów rozproszonych w środowisku chmurowym", level: "Magisterska", status: "Zajęty" },
  { id: 3, title: "Bezpieczeństwo systemów IoT opartych na Blockchain", level: "Inżynierska", status: "Dostępny" },
  { id: 4, title: "Analiza sentymentu w polskojęzycznych mediach społecznościowych", level: "Magisterska", status: "Dostępny" },
];

export const ProfilPromotora = () => {
  const { id } = useParams();

  // W prawdziwej aplikacji tutaj byłby useQuery pobierający dane po id
  const promotor = {
    name: "prof. dr hab. Jan Kowalski",
    department: "Katedra Systemów Informatycznych",
    email: "jan.kowalski@pwr.edu.pl",
    room: "D-1, pok. 211",
    rating: "4.9",
    totalStudents: 124,
    freeSpots: 3,
    bio: "Od ponad 15 lat zajmuję się sztuczną inteligencją oraz przetwarzaniem języka naturalnego. Współpracuję z czołowymi ośrodkami badawczymi w Europie. W pracach dyplomowych cenię samodzielność, innowacyjne podejście do problemów oraz rzetelność w przeprowadzaniu badań.",
    avatar: `https://i.pravatar.cc/150?u=${id || 20}`
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <Breadcrumbs className="mb-2">
        <BreadcrumbItem as={RouterLink} to="/promotorzy">Promotorzy</BreadcrumbItem>
        <BreadcrumbItem>Profil Profila</BreadcrumbItem>
      </Breadcrumbs>

      {/* Hero Section Container */}
      <div className="flex flex-col lg:flex-row gap-8">
        
        {/* Left Side: Avatar & Core Info */}
        <div className="w-full lg:w-1/3 flex flex-col gap-6">
          <Card className="p-8 border-none bg-gradient-to-br from-slate-900 to-slate-800 text-white shadow-2xl rounded-[2.5rem]">
            <CardBody className="flex flex-col items-center gap-6 text-center">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="relative"
              >
                <div className="absolute -inset-4 bg-primary/20 rounded-full blur-xl animate-pulse" />
                <User
                  name=""
                  avatarProps={{
                    src: promotor.avatar,
                    className: "w-32 h-32 text-large border-4 border-white/10",
                    isBordered: true,
                    radius: "full",
                    color: "primary"
                  }}
                />
                <Chip color="success" variant="shadow" className="absolute -bottom-2 left-1/2 -translate-x-1/2 font-black uppercase text-[10px] bg-white text-slate-900 border-none">
                   Aktywny
                </Chip>
              </motion.div>
              
              <div className="space-y-2">
                <h2 className="text-2xl font-black tracking-tight leading-none">{promotor.name}</h2>
                <p className="text-primary font-bold text-sm uppercase tracking-widest leading-none">{promotor.department}</p>
              </div>

              <div className="flex gap-4 mt-2">
                 <Button isIconOnly variant="flat" className="bg-white/5 rounded-xl hover:bg-white/10 text-white border-none"><Globe size={20} /></Button>
                 <Button isIconOnly variant="flat" className="bg-white/5 rounded-xl hover:bg-white/10 text-white border-none"><Link2 size={20} /></Button>
              </div>

              <Divider className="bg-white/10 my-2" />

              <div className="w-full space-y-4">
                 <div className="flex items-center gap-3 text-slate-300">
                    <div className="bg-white/5 p-2 rounded-lg"><Mail size={16} /></div>
                    <span className="text-sm font-medium">{promotor.email}</span>
                 </div>
                 <div className="flex items-center gap-3 text-slate-300">
                    <div className="bg-white/5 p-2 rounded-lg"><MapPin size={16} /></div>
                    <span className="text-sm font-medium">{promotor.room}</span>
                 </div>
              </div>

              <Button color="primary" fullWidth size="lg" className="h-16 font-black text-lg shadow-xl shadow-primary/20 mt-4 rounded-2xl bg-white text-slate-900">
                Wybierz Promotora
              </Button>
            </CardBody>
          </Card>

          <Card className="border-none shadow-xl rounded-[2rem]">
             <CardBody className="p-6 flex flex-col gap-6">
                <h3 className="font-black text-xl text-slate-800">Dostępność Miejsc</h3>
                <div className="space-y-4">
                   <div className="flex justify-between items-end">
                      <span className="text-4xl font-black text-primary">{promotor.freeSpots}</span>
                      <span className="text-xs font-bold text-default-400 uppercase tracking-widest pb-1">Miejsca Wolne</span>
                   </div>
                   <Progress 
                      value={(promotor.freeSpots / 10) * 100} 
                      color={promotor.freeSpots > 2 ? "primary" : "danger"} 
                      className="h-2"
                   />
                   <p className="text-xs text-default-400 font-medium italic">Ostatnia aktualizacja: przed chwilą</p>
                </div>
             </CardBody>
          </Card>
        </div>

        {/* Right Side: Detailed Content */}
        <div className="w-full lg:w-2/3 flex flex-col gap-6">
          
          <Card className="border-none shadow-xl rounded-[2.5rem] bg-white/70 backdrop-blur-md">
            <CardBody className="p-8">
              <Tabs 
                variant="underlined" 
                color="primary" 
                classNames={{
                  tabList: "gap-8",
                  cursor: "w-full bg-primary h-1 rounded-full",
                  tab: "max-w-fit px-0 h-12 text-md font-black uppercase tracking-widest",
                }}
              >
                <Tab
                  key="bio"
                  title={
                    <div className="flex items-center space-x-2">
                      <FileText size={18} />
                      <span>O mnie</span>
                    </div>
                  }
                >
                  <div className="py-8 space-y-6">
                    <h3 className="text-2xl font-black text-slate-800">Zainteresowania Badawcze</h3>
                    <p className="text-default-600 text-lg leading-relaxed">
                      {promotor.bio}
                    </p>
                    <div className="grid grid-cols-2 gap-4">
                       <div className="p-6 bg-default-50 rounded-2xl border border-default-100">
                          <div className="text-primary font-black text-3xl mb-1">{promotor.totalStudents}</div>
                          <div className="text-[10px] font-black uppercase text-default-400 tracking-widest">Wypromowanych</div>
                       </div>
                       <div className="p-6 bg-default-50 rounded-2xl border border-default-100">
                          <div className="text-warning font-black text-3xl mb-1">{promotor.rating}</div>
                          <div className="text-[10px] font-black uppercase text-default-400 tracking-widest">Średnia Ocen</div>
                       </div>
                    </div>
                  </div>
                </Tab>

                <Tab
                  key="topics"
                  title={
                    <div className="flex items-center space-x-2">
                      <GraduationCap size={18} />
                      <span>Tematy Prac</span>
                    </div>
                  }
                >
                  <div className="py-8 flex flex-col gap-4">
                    {DUMMY_TOPICS.map((topic) => (
                      <Card key={topic.id} className="border border-default-100 bg-white/50 hover:bg-white hover:shadow-lg transition-all p-4 group cursor-pointer rounded-2xl">
                        <CardBody className="flex flex-row justify-between items-center p-2">
                           <div className="flex flex-col gap-1">
                              <h4 className="font-bold text-slate-800 group-hover:text-primary transition-colors">{topic.title}</h4>
                              <div className="flex gap-2 items-center">
                                 <Chip size="sm" variant="flat" color="secondary" className="border-none font-bold text-[10px]">{topic.level}</Chip>
                                 <span className="text-[10px] text-default-400 font-bold uppercase tracking-tighter flex items-center gap-1">
                                    <Calendar size={10} /> Rok akad. 2025/26
                                 </span>
                              </div>
                           </div>
                           <Chip 
                              color={topic.status === "Dostępny" ? "success" : "danger"} 
                              variant="dot" 
                              className="border-none font-bold"
                           >
                              {topic.status}
                           </Chip>
                        </CardBody>
                      </Card>
                    ))}
                  </div>
                </Tab>

                <Tab
                  key="contact"
                  title={
                    <div className="flex items-center space-x-2">
                      <MessageSquare size={18} />
                      <span>Kontakt</span>
                    </div>
                  }
                >
                   <div className="py-8 space-y-8">
                      <div className="bg-primary-50 p-8 rounded-3xl border-2 border-dashed border-primary/20">
                         <h4 className="text-xl font-black text-primary mb-2">Konsultacje Czwartkowe</h4>
                         <p className="text-default-700 font-medium">Spotkania odbywają się w każdą środę w godzinach 10:00 - 12:00. <br />Możliwe są również spotkania przez MS Teams po wcześniejszym umówieniu.</p>
                      </div>
                      <div className="flex flex-col gap-4">
                         <Button color="primary" size="lg" className="h-16 font-black text-lg rounded-2xl shadow-xl shadow-primary/20" startContent={<MessageSquare size={20} />}>
                            Umów się na spotkanie
                         </Button>
                         <Button variant="bordered" size="lg" className="h-16 font-black text-lg rounded-2xl border-2 border-default-200">
                            Napisz wiadomość E-mail
                         </Button>
                      </div>
                   </div>
                </Tab>
              </Tabs>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
};
