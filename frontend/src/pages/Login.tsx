import { Card, CardHeader, CardBody, Divider, Input, Button, Tabs, Tab, Link } from "@nextui-org/react";
import { Mail, Lock, User as UserIcon, Key, GraduationCap } from "lucide-react";
import { Link as RouterLink } from "react-router-dom";
import { motion } from "framer-motion";

export const Login = () => {
  return (
    <section className="mt-12 flex justify-center items-center py-20 bg-dot-slate-200">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-md p-4"
      >
        <Card className="p-4 shadow-2xl border border-default-100 rounded-3xl bg-white/90 backdrop-blur-xl">
          <CardHeader className="flex flex-col gap-1 items-center pb-8 pt-6">
            <div className="bg-primary/10 p-4 rounded-2xl mb-4 text-primary">
              <GraduationCap size={48} strokeWidth={1.5} />
            </div>
            <h1 className="text-3xl font-black tracking-tight text-slate-800">Cześć ponownie!</h1>
            <p className="text-default-500 font-medium">Zaloguj się do swojego profilu</p>
          </CardHeader>
          <CardBody className="pt-0">
            <Tabs
              fullWidth
              size="lg"
              variant="underlined"
              color="primary"
              aria-label="Login Tabs"
              className="pb-6"
            >
              <Tab
                key="student"
                title={
                  <div className="flex items-center space-x-2">
                    <UserIcon size={18} />
                    <span>Student</span>
                  </div>
                }
              >
                <form className="flex flex-col gap-4 pt-6">
                  <Input
                    label="E-mail"
                    placeholder="Wpisz swój e-mail"
                    variant="bordered"
                    labelPlacement="outside"
                    size="lg"
                    startContent={<Mail className="text-default-400 pointer-events-none" size={20} />}
                  />
                  <Input
                    label="Hasło"
                    placeholder="Wpisz hasło"
                    variant="bordered"
                    labelPlacement="outside"
                    size="lg"
                    type="password"
                    startContent={<Lock className="text-default-400 pointer-events-none" size={20} />}
                  />
                  <div className="flex justify-between items-center py-2">
                    <Link color="primary" href="#" size="sm" className="font-semibold italic">Zapomniałeś hasła?</Link>
                  </div>
                  <Button color="primary" size="lg" className="font-bold text-md shadow-lg shadow-primary/20 mt-4 rounded-2xl py-7" variant="shadow">
                    Dalej
                  </Button>
                </form>
              </Tab>
              <Tab
                key="promotor"
                title={
                  <div className="flex items-center space-x-2">
                    <GraduationCap size={18} />
                    <span>Promotor</span>
                  </div>
                }
              >
                <form className="flex flex-col gap-4 pt-6">
                   <Input
                    label="E-mail"
                    placeholder="Wpisz e-mail"
                    variant="bordered"
                    labelPlacement="outside"
                    size="lg"
                    startContent={<Mail className="text-default-400 pointer-events-none" size={20} />}
                  />
                  <Input
                    label="Klucz Pracownika"
                    placeholder="Twój kod dostępu"
                    variant="bordered"
                    labelPlacement="outside"
                    size="lg"
                    type="password"
                    startContent={<Lock className="text-default-400 pointer-events-none" size={20} />}
                  />
                  <Button color="primary" size="lg" className="font-bold text-md shadow-lg shadow-primary/20 mt-4 rounded-2xl py-7" variant="shadow">
                    Logowanie dla Pracowników
                  </Button>
                </form>
              </Tab>
            </Tabs>

            <Divider className="my-8" />

            <div className="flex flex-col gap-4">
              <Button
                variant="bordered"
                size="lg"
                className="font-bold border-default-200 text-slate-700 bg-slate-50/50"
                startContent={<Key size={20} />}
              >
                Kontynuuj z LDAP (Pracownicy)
              </Button>
              <p className="text-center text-sm text-default-400 font-medium">
                Nie masz konta? <Link as={RouterLink} to="/rejestracja" size="sm" className="font-bold underline decoration-2 decoration-primary/30 underline-offset-4">Zarejestruj się</Link>
              </p>
            </div>
          </CardBody>
        </Card>
      </motion.div>
    </section>
  );
};
