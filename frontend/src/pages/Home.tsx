import {
  Card,
  CardHeader,
  CardBody,
  Divider,
  Chip,
  Button,
} from "@nextui-org/react";
import { Layout as LayoutIcon, Database, Server, CheckCircle2, ArrowRight, MousePointer2, Zap, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const architecture = [
  {
    layer: "Frontend",
    tech: "React + NextUI",
    desc: "Zaprojektowany z myślą o urządzeniach mobilnych i komuterach, z płynnymi przejściami.",
    icon: <LayoutIcon className="text-blue-500" size={24} />,
  },
  {
    layer: "Backend",
    tech: "FastAPI + Python",
    desc: "Wydajny silnik wspierający tysiące równoczesnych wniosków studenckich.",
    icon: <Server className="text-green-500" size={24} />,
  },
  {
    layer: "Bezpieczeństwo",
    tech: "JWT + LDAP",
    desc: "Zintegrowane systemy logowania uczelnianego zapewniające ochronę Twoich danych.",
    icon: <ShieldCheck className="text-indigo-500" size={24} />,
  },
];

const ScrollSection = ({ children, delay = 0 }: { children: React.ReactNode, delay?: number }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-100px" }}
    transition={{ duration: 0.8, delay, ease: "easeOut" }}
  >
    {children}
  </motion.div>
);

export const Home = () => {
  return (
    <div className="relative overflow-hidden min-h-screen">
      {/* Background Animated Blobs */}
      <div className="absolute top-0 left-0 w-full h-full -z-10 pointer-events-none">
        <motion.div 
          animate={{ scale: [1, 1.2, 1], x: [0, 50, 0], y: [0, -30, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-400/20 rounded-full blur-[120px]" 
        />
        <motion.div 
          animate={{ scale: [1, 1.3, 1], x: [0, -40, 0], y: [0, 60, 0] }}
          transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }}
          className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-[150px]" 
        />
      </div>

      <header className="mb-24 mt-12 text-center max-w-4xl mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
        >
          <Chip
            color="primary"
            variant="shadow"
            className="mb-8 px-6 py-4 uppercase font-black tracking-widest bg-gradient-to-r from-blue-600 to-indigo-600 shadow-xl"
            size="lg"
          >
            Przyszłość Edukacji Wyższej
          </Chip>
        </motion.div>

        <motion.h1 
          className="text-6xl md:text-8xl font-black tracking-tighter mb-8 leading-[0.9]"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
        >
          Twój Wybór, <br />
          <span className="bg-gradient-to-r from-blue-600 via-indigo-500 to-primary bg-clip-text text-transparent">Twoja Kariera</span>
        </motion.h1>

        <motion.p 
          className="text-xl md:text-2xl text-default-500 leading-relaxed max-w-2xl mx-auto mb-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          Pierwszy w pełni zautomatyzowany system przydziału promotorów, który stawia Twoje preferencje na pierwszym miejscu.
        </motion.p>

        <motion.div 
          className="flex flex-col sm:flex-row gap-6 justify-center"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Button
            as={Link}
            to="/login"
            color="primary"
            size="lg"
            className="h-16 px-12 font-black text-lg bg-gradient-to-r from-blue-600 to-indigo-600 shadow-2xl shadow-blue-500/40 rounded-3xl group"
            endContent={<ArrowRight size={20} className="group-hover:translate-x-2 transition-transform" />}
          >
            Zacznij Przygodę
          </Button>
          <Button
            as={Link}
            to="/promotorzy"
            variant="flat"
            size="lg"
            className="h-16 px-12 font-black text-lg backdrop-blur-md rounded-3xl"
            startContent={<MousePointer2 size={20} />}
          >
            Lista Ekspertów
          </Button>
        </motion.div>
      </header>

      {/* Feature Section with Scroll Reveal */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-32 px-4">
        {architecture.map((item, idx) => (
          <ScrollSection key={item.layer} delay={idx * 0.2}>
            <Card
              className="p-8 h-full bg-white/40 backdrop-blur-xl border border-white/50 shadow-sm hover:shadow-2xl hover:bg-white transition-all duration-500 rounded-[2.5rem]"
              isPressable
            >
              <CardHeader className="flex flex-col items-start gap-4 pb-4">
                <div className="bg-primary/10 p-5 rounded-2xl text-primary">
                  {item.icon}
                </div>
                <div>
                   <h2 className="text-2xl font-black text-slate-800">{item.layer}</h2>
                   <Chip color="primary" variant="flat" size="sm" className="mt-1 font-bold border-none uppercase text-[10px]">{item.tech}</Chip>
                </div>
              </CardHeader>
              <CardBody className="pt-2">
                <p className="text-default-500 font-medium leading-relaxed">
                  {item.desc}
                </p>
              </CardBody>
            </Card>
          </ScrollSection>
        ))}
      </section>

      {/* Powerful Call to Action Section */}
      <ScrollSection>
        <div className="bg-slate-900 rounded-[3rem] p-12 md:p-24 relative overflow-hidden text-center md:text-left mb-32 shadow-2xl mx-4">
           {/* CTA Blobs */}
           <div className="absolute top-0 right-0 w-96 h-96 bg-primary/30 rounded-full -mr-48 -mt-48 blur-3xl animate-pulse" />
           <div className="absolute bottom-0 left-0 w-64 h-64 bg-indigo-500/20 rounded-full -ml-32 -mb-32 blur-3xl animate-pulse" />
           
           <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-12">
              <div className="max-w-xl flex flex-col gap-6">
                 <div className="flex items-center gap-2 text-primary font-black uppercase tracking-[0.2em] text-sm">
                    <Zap size={20} className="fill-primary" /> Technologia Jutra
                 </div>
                 <h2 className="text-5xl md:text-6xl font-black text-white tracking-tighter leading-none">
                    Gotowy na <br /> <span className="underline decoration-primary decoration-4 underline-offset-8 italic">etap dyplomowy?</span>
                 </h2>
                 <p className="text-slate-400 text-xl font-medium leading-relaxed">
                    Nasz system to nie tylko przydział – to Twój start w profesjonalny świat nauki. Dołącz do tysięcy studentów, którzy już wybrali swoich mistrzów.
                 </p>
              </div>
              <div className="bg-white/5 p-10 rounded-[2.5rem] border border-white/5 backdrop-blur-3xl flex flex-col gap-6 w-full md:w-auto min-w-[300px]">
                 <div className="flex flex-col text-center">
                    <span className="text-4xl font-black text-white leading-none mb-2 tracking-tighter">800+</span>
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Aktywnych Tematów</span>
                 </div>
                 <Divider className="bg-white/10" />
                 <div className="flex flex-col text-center">
                    <span className="text-4xl font-black text-primary leading-none mb-2 tracking-tighter">100%</span>
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Gwarancja Wyboru</span>
                 </div>
                 <Button color="primary" size="lg" className="h-16 font-black text-lg rounded-2xl shadow-xl shadow-primary/20">
                    Otwórz Panel
                 </Button>
              </div>
           </div>
        </div>
      </ScrollSection>
    </div>
  );
};
