import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "Dashboard", icon: "dashboard" },
  { to: "/customers", label: "Clientes", icon: "customers" },
  { to: "/quotations", label: "Cotizaciones", icon: "quotations" },
];

function NavIcon({ name }) {
  const paths = {
    dashboard: (
      <>
        <rect x="3" y="3" width="7" height="7" rx="2" />
        <rect x="14" y="3" width="7" height="7" rx="2" />
        <rect x="3" y="14" width="7" height="7" rx="2" />
        <rect x="14" y="14" width="7" height="7" rx="2" />
      </>
    ),
    customers: (
      <>
        <path d="M16 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2" />
        <circle cx="9.5" cy="7" r="4" />
        <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </>
    ),
    quotations: (
      <>
        <path d="M7 3h8l4 4v14H7z" />
        <path d="M15 3v5h5" />
        <path d="M10 12h6" />
        <path d="M10 16h6" />
      </>
    ),
  };

  return (
    <svg
      aria-hidden="true"
      className="h-5 w-5"
      fill="none"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="1.8"
      viewBox="0 0 24 24"
    >
      {paths[name]}
    </svg>
  );
}

export default function Sidebar() {
  return (
    <aside className="flex w-full flex-col border-b border-rose-100 bg-[#fff1f5]/95 px-5 py-5 shadow-sm lg:min-h-screen lg:w-72 lg:border-b-0 lg:border-r lg:px-6 lg:py-7">
      <div>
        <p className="text-xs font-bold uppercase text-rose-400">
          Bakery Studio
        </p>
        <h1 className="mt-2 text-3xl font-black leading-none text-stone-800">
          Flor de
          <span className="block text-rose-500">Vainilla</span>
        </h1>
      </div>

      <nav className="mt-7 grid gap-2 sm:grid-cols-3 lg:flex lg:flex-col">
        {navItems.map((item) => (
          <NavLink
            className={({ isActive }) =>
              [
                "flex min-h-12 items-center gap-3 rounded-xl px-4 py-3 text-sm font-bold transition",
                isActive
                  ? "bg-white text-rose-600 shadow-sm ring-1 ring-rose-100"
                  : "text-stone-600 hover:bg-white/70 hover:text-stone-900",
              ].join(" ")
            }
            end={item.to === "/"}
            key={item.to}
            to={item.to}
          >
            <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-rose-100 text-rose-500">
              <NavIcon name={item.icon} />
            </span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto hidden rounded-2xl bg-white p-4 text-sm text-stone-500 shadow-sm ring-1 ring-rose-100 lg:block">
        <p className="font-bold text-stone-700">Resumen del dia</p>
        <p className="mt-1">4 pedidos listos para revisar.</p>
      </div>
    </aside>
  );
}
