import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import heroImage from "../assets/hero.png";
import MainLayout from "../components/layout/MainLayout";
import { getCustomers } from "../services/customerService";
import { getDashboardStats } from "../services/dashboardService";
import { getQuotations } from "../services/quotationService";
import { formatCurrency, formatDate, statusLabel } from "../utils/formatters";

function StatCard({ detail, label, tone, value }) {
  const tones = {
    amber: "bg-amber-50 text-amber-700 ring-amber-100",
    emerald: "bg-emerald-50 text-emerald-700 ring-emerald-100",
    rose: "bg-rose-50 text-rose-700 ring-rose-100",
  };

  return (
    <article className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-bold text-stone-500">{label}</p>
          <p className="mt-3 text-4xl font-black text-stone-900">{value}</p>
        </div>
        <span className={`rounded-full px-3 py-1 text-xs font-bold ${tones[tone]}`}>
          {detail}
        </span>
      </div>
    </article>
  );
}

function EmptyState({ children }) {
  return (
    <div className="rounded-xl bg-[#fff8f3] p-4 text-sm font-bold text-stone-500">
      {children}
    </div>
  );
}

export default function Dashboard() {
  const [customers, setCustomers] = useState([]);
  const [dashboardStats, setDashboardStats] = useState({
    customers: 0,
    quotations: 0,
    sales: 0,
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [quotations, setQuotations] = useState([]);

  useEffect(() => {
    let ignore = false;

    async function loadDashboard() {
      try {
        const [statsData, quotationData, customerData] = await Promise.all([
          getDashboardStats(),
          getQuotations(),
          getCustomers(),
        ]);

        if (!ignore) {
          setDashboardStats(statsData);
          setQuotations(quotationData);
          setCustomers(customerData);
        }
      } catch {
        if (!ignore) {
          setError("No se pudo cargar la informacion del backend.");
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      ignore = true;
    };
  }, []);

  const customersById = useMemo(
    () => new Map(customers.map((customer) => [customer.customer_id, customer])),
    [customers]
  );

  const sortedQuotations = useMemo(
    () =>
      [...quotations].sort(
        (a, b) => new Date(b.quotation_date) - new Date(a.quotation_date)
      ),
    [quotations]
  );

  const pendingQuotes = useMemo(
    () => sortedQuotations.filter((quote) => quote.status === "pending").slice(0, 4),
    [sortedQuotations]
  );

  const pendingCount = quotations.filter((quote) => quote.status === "pending").length;
  const recentQuotes = sortedQuotations.slice(0, 4);

  const topCustomers = useMemo(
    () =>
      customers
        .map((customer) => ({
          ...customer,
          quotationCount: quotations.filter(
            (quote) => quote.customer_id === customer.customer_id
          ).length,
        }))
        .sort((a, b) => b.quotationCount - a.quotationCount)
        .slice(0, 3),
    [customers, quotations]
  );

  const stats = [
    {
      detail: `${pendingCount} pendientes`,
      label: "Cotizaciones",
      tone: "rose",
      value: dashboardStats.quotations,
    },
    {
      detail: "registrados",
      label: "Clientes",
      tone: "amber",
      value: dashboardStats.customers,
    },
    {
      detail: "total cotizado",
      label: "Ingresos",
      tone: "emerald",
      value: formatCurrency(dashboardStats.sales),
    },
  ];

  const action = (
    <div className="flex flex-wrap gap-2">
      <Link
        className="rounded-xl bg-white px-4 py-3 text-sm font-black text-stone-700 ring-1 ring-rose-100 transition hover:bg-rose-50"
        to="/quotations"
      >
        Ver cotizaciones
      </Link>
      <Link
        className="rounded-xl bg-rose-500 px-4 py-3 text-sm font-black text-white shadow-sm transition hover:bg-rose-600"
        to="/quotations/new"
      >
        Nueva cotizacion
      </Link>
    </div>
  );

  return (
    <MainLayout
      action={action}
      subtitle="Acceso rapido a cotizaciones, clientes y pedidos personalizados"
      title="Dashboard"
    >
      {error && (
        <div className="mb-6 rounded-2xl bg-red-50 p-4 text-sm font-bold text-red-700 ring-1 ring-red-100">
          {error}
        </div>
      )}

      <section className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
        <div className="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-rose-100">
          <div className="grid gap-6 p-6 lg:grid-cols-[1fr_300px] lg:p-8">
            <div className="flex flex-col justify-center">
              <p className="text-sm font-bold uppercase text-rose-400">
                Panel de produccion
              </p>
              <h1 className="mt-3 max-w-2xl text-4xl font-black leading-tight text-stone-900 sm:text-5xl">
                Revisa y abre cotizaciones sin perder tiempo.
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-stone-600">
                Entra directo al listado, abre la siguiente pendiente o crea una nueva desde aqui.
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Link
                  className="rounded-xl bg-stone-900 px-5 py-3 text-sm font-black text-white transition hover:bg-stone-700"
                  to="/quotations"
                >
                  Ver todas las cotizaciones
                </Link>
                {pendingQuotes[0] && (
                  <Link
                    className="rounded-xl bg-amber-50 px-5 py-3 text-sm font-black text-amber-800 ring-1 ring-amber-100 transition hover:bg-amber-100"
                    to={`/quotations/${pendingQuotes[0].quotation_id}`}
                  >
                    Abrir pendiente #{pendingQuotes[0].quotation_id}
                  </Link>
                )}
                <Link
                  className="rounded-xl bg-rose-50 px-5 py-3 text-sm font-black text-rose-700 ring-1 ring-rose-100 transition hover:bg-rose-100"
                  to="/customers"
                >
                  Ver clientes
                </Link>
              </div>
            </div>

            <div className="relative min-h-64 rounded-2xl bg-[#fff3f0] p-6">
              <div className="absolute inset-x-8 bottom-6 h-20 rounded-full bg-rose-200/60 blur-2xl" />
              <img
                alt="Flor de Vainilla"
                className="relative z-10 mx-auto h-60 w-full object-contain"
                src={heroImage}
              />
            </div>
          </div>
        </div>

        <aside className="rounded-2xl bg-[#3b2a28] p-6 text-white shadow-sm">
          <p className="text-sm font-bold uppercase text-rose-200">Pendientes</p>
          <p className="mt-4 text-4xl font-black">{loading ? "..." : pendingCount}</p>
          <p className="mt-2 text-sm leading-6 text-rose-50/80">
            cotizaciones necesitan seguimiento antes del cierre.
          </p>

          <div className="mt-6 space-y-3">
            {pendingQuotes[0] && (
              <Link
                className="block rounded-xl bg-white p-4 text-stone-800 transition hover:bg-rose-50"
                to={`/quotations/${pendingQuotes[0].quotation_id}`}
              >
                <p className="text-xs font-bold uppercase text-rose-500">
                  Siguiente por revisar
                </p>
                <p className="mt-1 font-black">
                  Cotizacion #{pendingQuotes[0].quotation_id}
                </p>
                <p className="text-sm text-stone-500">
                  {customersById.get(pendingQuotes[0].customer_id)?.name ||
                    "Cliente no disponible"}
                </p>
              </Link>
            )}

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-xl bg-white/10 p-4">
                <p className="font-bold">Aprobadas</p>
                <p className="text-sm text-rose-50/75">
                  {quotations.filter((quote) => quote.status === "approved").length}
                </p>
              </div>
              <div className="rounded-xl bg-white/10 p-4">
                <p className="font-bold">Canceladas</p>
                <p className="text-sm text-rose-50/75">
                  {quotations.filter((quote) => quote.status === "canceled").length}
                </p>
              </div>
            </div>
          </div>
        </aside>
      </section>

      <section className="mt-6 grid gap-6 md:grid-cols-3">
        {stats.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </section>

      <section className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <article className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-xl font-black text-stone-900">Cotizaciones recientes</h2>
              <p className="text-sm text-stone-500">
                Abre cualquier detalle en un toque.
              </p>
            </div>
            <Link className="text-sm font-bold text-rose-600 hover:text-rose-700" to="/quotations">
              Ver tabla completa
            </Link>
          </div>

          <div className="mt-5 divide-y divide-rose-100">
            {recentQuotes.length === 0 && (
              <EmptyState>No hay cotizaciones registradas todavia.</EmptyState>
            )}

            {recentQuotes.map((quote) => (
              <div
                className="flex flex-col gap-3 py-4 sm:flex-row sm:items-center sm:justify-between"
                key={quote.quotation_id}
              >
                <div>
                  <p className="font-bold text-stone-800">
                    Cotizacion #{quote.quotation_id}
                  </p>
                  <p className="text-sm text-stone-500">
                    {customersById.get(quote.customer_id)?.name || "Cliente no disponible"} /{" "}
                    {formatDate(quote.quotation_date)} / {statusLabel(quote.status)}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <p className="font-black text-rose-600">{formatCurrency(quote.total)}</p>
                  <Link
                    className="rounded-lg bg-stone-900 px-3 py-2 text-xs font-black text-white transition hover:bg-stone-700"
                    to={`/quotations/${quote.quotation_id}`}
                  >
                    Detalle
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-xl font-black text-stone-900">Pendientes rapidas</h2>
            <Link className="text-sm font-bold text-rose-600 hover:text-rose-700" to="/quotations">
              Ver todo
            </Link>
          </div>

          <div className="mt-5 space-y-3">
            {pendingQuotes.length === 0 && (
              <EmptyState>No hay cotizaciones pendientes.</EmptyState>
            )}

            {pendingQuotes.map((quote) => (
              <Link
                className="flex items-center justify-between gap-4 rounded-xl bg-[#fff8f3] p-4 transition hover:bg-rose-50"
                key={quote.quotation_id}
                to={`/quotations/${quote.quotation_id}`}
              >
                <div>
                  <p className="font-bold text-stone-800">#{quote.quotation_id}</p>
                  <p className="text-sm text-stone-500">
                    {customersById.get(quote.customer_id)?.name || "Cliente no disponible"}
                  </p>
                </div>
                <span className="rounded-full bg-white px-3 py-1 text-xs font-bold text-stone-600 ring-1 ring-rose-100">
                  {formatCurrency(quote.total)}
                </span>
              </Link>
            ))}
          </div>
        </article>
      </section>

      <section className="mt-6">
        <article className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-xl font-black text-stone-900">Clientes destacados</h2>
            <Link className="text-sm font-bold text-rose-600 hover:text-rose-700" to="/customers">
              Ver todo
            </Link>
          </div>

          <div className="mt-5 grid gap-3 md:grid-cols-3">
            {topCustomers.length === 0 && (
              <EmptyState>No hay clientes registrados todavia.</EmptyState>
            )}

            {topCustomers.map((customer) => (
              <div
                className="flex items-center justify-between gap-4 rounded-xl bg-[#fff8f3] p-4"
                key={customer.customer_id}
              >
                <div>
                  <p className="font-bold text-stone-800">{customer.name}</p>
                  <p className="text-sm text-stone-500">{customer.phone}</p>
                </div>
                <span className="rounded-full bg-white px-3 py-1 text-xs font-bold text-stone-600 ring-1 ring-rose-100">
                  {customer.quotationCount} cotizaciones
                </span>
              </div>
            ))}
          </div>
        </article>
      </section>
    </MainLayout>
  );
}
