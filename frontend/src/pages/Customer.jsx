import { useEffect, useMemo, useState } from "react";

import MainLayout from "../components/layout/MainLayout";
import { getCustomers } from "../services/customerService";
import { getQuotations } from "../services/quotationService";

export default function Customers() {
  const [customers, setCustomers] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [quotations, setQuotations] = useState([]);

  useEffect(() => {
    let ignore = false;

    async function loadCustomers() {
      try {
        const [customerData, quotationData] = await Promise.all([
          getCustomers(),
          getQuotations(),
        ]);

        if (!ignore) {
          setCustomers(customerData);
          setQuotations(quotationData);
        }
      } catch {
        if (!ignore) {
          setError("No se pudieron cargar los clientes.");
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    loadCustomers();

    return () => {
      ignore = true;
    };
  }, []);

  const customersWithTotals = useMemo(
    () =>
      customers.map((customer) => ({
        ...customer,
        quotationCount: quotations.filter(
          (quote) => quote.customer_id === customer.customer_id
        ).length,
      })),
    [customers, quotations]
  );

  return (
    <MainLayout
      subtitle="Directorio rapido para dar seguimiento a pedidos y cotizaciones"
      title="Clientes"
    >
      <section className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-black text-stone-900">Clientes</h1>
            <p className="mt-1 text-sm text-stone-500">
              Datos leidos de la tabla customer.
            </p>
          </div>

          <span className="rounded-xl bg-rose-50 px-4 py-3 text-sm font-black text-rose-700 ring-1 ring-rose-100">
            {loading ? "Cargando..." : `${customers.length} clientes`}
          </span>
        </div>

        {error && (
          <div className="mt-6 rounded-2xl bg-red-50 p-4 text-sm font-bold text-red-700 ring-1 ring-red-100">
            {error}
          </div>
        )}

        <div className="mt-6 overflow-hidden rounded-2xl ring-1 ring-rose-100">
          <table className="w-full min-w-[760px] border-collapse text-left text-sm">
            <thead className="bg-[#fff1f5] text-xs uppercase text-rose-500">
              <tr>
                <th className="px-5 py-4 font-black">Cliente</th>
                <th className="px-5 py-4 font-black">Telefono</th>
                <th className="px-5 py-4 font-black">Direccion</th>
                <th className="px-5 py-4 font-black">Cotizaciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-rose-100 bg-white">
              {!loading && customersWithTotals.length === 0 && (
                <tr>
                  <td className="px-5 py-6 text-center font-bold text-stone-500" colSpan="4">
                    No hay clientes registrados en la base de datos.
                  </td>
                </tr>
              )}

              {customersWithTotals.map((customer) => (
                <tr className="transition hover:bg-[#fff8f3]" key={customer.customer_id}>
                  <td className="px-5 py-4 font-bold text-stone-800">{customer.name}</td>
                  <td className="px-5 py-4 text-stone-500">{customer.phone}</td>
                  <td className="px-5 py-4 text-stone-500">
                    {customer.address || "Sin direccion"}
                  </td>
                  <td className="px-5 py-4">
                    <span className="rounded-full bg-amber-50 px-3 py-1 font-bold text-amber-700">
                      {customer.quotationCount}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </MainLayout>
  );
}
