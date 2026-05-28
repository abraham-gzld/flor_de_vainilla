import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import MainLayout from "../components/layout/MainLayout";
import { getCustomers } from "../services/customerService";
import { getFullQuotation, getQuotations } from "../services/quotationService";
import {
  formatCurrency,
  formatDate,
  quotationDetailDescription,
  quotationDetailTitle,
  statusLabel,
} from "../utils/formatters";

const statuses = ["pending", "approved", "canceled"];

export default function Quotations() {
  const [customers, setCustomers] = useState([]);
  const [detailError, setDetailError] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [quickDetail, setQuickDetail] = useState(null);
  const [quotations, setQuotations] = useState([]);
  const [selectedQuotationId, setSelectedQuotationId] = useState(null);

  useEffect(() => {
    let ignore = false;

    async function loadQuotations() {
      try {
        const [quotationData, customerData] = await Promise.all([
          getQuotations(),
          getCustomers(),
        ]);

        if (!ignore) {
          const sortedData = [...quotationData].sort(
            (a, b) => new Date(b.quotation_date) - new Date(a.quotation_date)
          );

          setQuotations(quotationData);
          setCustomers(customerData);
          setSelectedQuotationId((current) =>
            current || sortedData[0]?.quotation_id || null
          );
        }
      } catch {
        if (!ignore) {
          setError("No se pudieron cargar las cotizaciones.");
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    loadQuotations();

    return () => {
      ignore = true;
    };
  }, []);

  useEffect(() => {
    if (!selectedQuotationId) {
      return undefined;
    }

    let ignore = false;

    getFullQuotation(selectedQuotationId)
      .then((data) => {
        if (!ignore) {
          setQuickDetail(data);
          setDetailError("");
        }
      })
      .catch(() => {
        if (!ignore) {
          setDetailError("No se pudo cargar la vista rapida.");
        }
      });

    return () => {
      ignore = true;
    };
  }, [selectedQuotationId]);

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

  const selectedDetail =
    quickDetail?.quotation_id === selectedQuotationId ? quickDetail : null;

  function selectQuotation(id) {
    setDetailError("");
    setQuickDetail(null);
    setSelectedQuotationId(id);
  }

  const action = (
    <Link
      className="rounded-xl bg-rose-500 px-4 py-3 text-sm font-black text-white shadow-sm transition hover:bg-rose-600"
      to="/quotations/new"
    >
      Nueva cotizacion
    </Link>
  );

  return (
    <MainLayout
      action={action}
      subtitle="Consulta la tabla y revisa lo incluido sin salir de esta pantalla"
      title="Cotizaciones"
    >
      {error && (
        <div className="mb-6 rounded-2xl bg-red-50 p-4 text-sm font-bold text-red-700 ring-1 ring-red-100">
          {error}
        </div>
      )}

      <section className="grid gap-6 xl:grid-cols-[0.72fr_1.28fr]">
        <aside className="grid gap-6">
          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
            <h1 className="text-3xl font-black text-stone-900">Pipeline</h1>
            <p className="mt-2 text-sm leading-6 text-stone-500">
              Toca cualquier cotizacion para verla en el panel rapido.
            </p>

            <div className="mt-6 grid gap-3">
              {statuses.map((status) => (
                <div className="rounded-xl bg-[#fff8f3] p-4" key={status}>
                  <p className="text-sm font-bold text-stone-700">{statusLabel(status)}</p>
                  <p className="mt-1 text-2xl font-black text-rose-600">
                    {quotations.filter((quote) => quote.status === status).length}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl bg-[#3b2a28] p-6 text-white shadow-sm">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-bold uppercase text-rose-200">
                  Vista rapida
                </p>
                <h2 className="mt-2 text-2xl font-black">
                  {selectedDetail
                    ? `Cotizacion #${selectedDetail.quotation_id}`
                    : "Selecciona una cotizacion"}
                </h2>
              </div>
              {selectedDetail && (
                <Link
                  className="rounded-lg bg-white px-3 py-2 text-xs font-black text-stone-800 transition hover:bg-rose-50"
                  to={`/quotations/${selectedDetail.quotation_id}`}
                >
                  Abrir
                </Link>
              )}
            </div>

            {detailError && (
              <div className="mt-5 rounded-xl bg-red-100 p-3 text-sm font-bold text-red-800">
                {detailError}
              </div>
            )}

            {!detailError && selectedQuotationId && !selectedDetail && (
              <div className="mt-5 rounded-xl bg-white/10 p-4 text-sm font-bold text-rose-50">
                Cargando detalle...
              </div>
            )}

            {!selectedQuotationId && (
              <div className="mt-5 rounded-xl bg-white/10 p-4 text-sm font-bold text-rose-50">
                No hay cotizaciones disponibles.
              </div>
            )}

            {selectedDetail && (
              <div className="mt-5 space-y-4">
                <div className="rounded-xl bg-white/10 p-4">
                  <p className="font-bold">{selectedDetail.customer?.name}</p>
                  <p className="text-sm text-rose-50/75">
                    {selectedDetail.customer?.phone || "Sin telefono"}
                  </p>
                  <p className="mt-2 text-sm text-rose-50/75">
                    {formatDate(selectedDetail.quotation_date)} /{" "}
                    {statusLabel(selectedDetail.status)}
                  </p>
                </div>

                <div className="rounded-xl bg-white p-4 text-stone-800">
                  <p className="text-xs font-bold uppercase text-rose-500">Total</p>
                  <p className="mt-1 text-3xl font-black">
                    {formatCurrency(selectedDetail.total)}
                  </p>
                </div>

                <div className="space-y-3">
                  {selectedDetail.details?.length === 0 && (
                    <div className="rounded-xl bg-white/10 p-4 text-sm font-bold text-rose-50">
                      Esta cotizacion no tiene partidas.
                    </div>
                  )}

                  {selectedDetail.details?.map((detail) => (
                    <div className="rounded-xl bg-white/10 p-4" key={detail.detail_id}>
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="font-bold">{quotationDetailTitle(detail)}</p>
                          <p className="mt-1 text-sm text-rose-50/75">
                            {quotationDetailDescription(detail)}
                          </p>
                          <p className="mt-1 text-xs font-bold uppercase text-rose-100">
                            Cantidad: {detail.quantity}
                          </p>
                        </div>
                        <span className="font-black">
                          {formatCurrency(detail.subtotal)}
                        </span>
                      </div>

                      {detail.custom_cake?.extras?.length > 0 && (
                        <div className="mt-3 flex flex-wrap gap-2">
                          {detail.custom_cake.extras.map((extra) => (
                            <span
                              className="rounded-full bg-white/15 px-3 py-1 text-xs font-bold text-rose-50"
                              key={extra.extra_id}
                            >
                              {extra.name}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </aside>

        <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-xl font-black text-stone-900">
                Todas las cotizaciones
              </h2>
              <p className="text-sm text-stone-500">
                Vista rapida para revisar contenido y boton para abrir detalle completo.
              </p>
            </div>
            <span className="rounded-xl bg-rose-50 px-4 py-3 text-sm font-black text-rose-700 ring-1 ring-rose-100">
              {loading ? "Cargando..." : `${sortedQuotations.length} registros`}
            </span>
          </div>

          <div className="mt-6 overflow-hidden rounded-2xl ring-1 ring-rose-100">
            <table className="w-full min-w-[940px] border-collapse text-left text-sm">
              <thead className="bg-[#fff1f5] text-xs uppercase text-rose-500">
                <tr>
                  <th className="px-5 py-4 font-black">Cotizacion</th>
                  <th className="px-5 py-4 font-black">Cliente</th>
                  <th className="px-5 py-4 font-black">Fecha</th>
                  <th className="px-5 py-4 font-black">Estado</th>
                  <th className="px-5 py-4 font-black">Total</th>
                  <th className="px-5 py-4 font-black">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-rose-100 bg-white">
                {!loading && sortedQuotations.length === 0 && (
                  <tr>
                    <td className="px-5 py-6 text-center font-bold text-stone-500" colSpan="6">
                      No hay cotizaciones registradas en la base de datos.
                    </td>
                  </tr>
                )}

                {sortedQuotations.map((quote) => {
                  const isSelected = selectedQuotationId === quote.quotation_id;

                  return (
                    <tr
                      className={`transition ${
                        isSelected ? "bg-rose-50" : "hover:bg-[#fff8f3]"
                      }`}
                      key={quote.quotation_id}
                    >
                      <td className="px-5 py-4">
                        <button
                          className="font-bold text-stone-800 hover:text-rose-600"
                          onClick={() => selectQuotation(quote.quotation_id)}
                          type="button"
                        >
                          #{quote.quotation_id}
                        </button>
                      </td>
                      <td className="px-5 py-4 text-stone-500">
                        {customersById.get(quote.customer_id)?.name ||
                          "Cliente no disponible"}
                      </td>
                      <td className="px-5 py-4 text-stone-500">
                        {formatDate(quote.quotation_date)}
                      </td>
                      <td className="px-5 py-4">
                        <span className="rounded-full bg-rose-50 px-3 py-1 font-bold text-rose-700">
                          {statusLabel(quote.status)}
                        </span>
                      </td>
                      <td className="px-5 py-4 font-black text-stone-900">
                        {formatCurrency(quote.total)}
                      </td>
                      <td className="px-5 py-4">
                        <div className="flex flex-wrap gap-2">
                          <button
                            className={`rounded-lg px-3 py-2 text-xs font-black transition ${
                              isSelected
                                ? "bg-rose-500 text-white"
                                : "bg-rose-50 text-rose-700 hover:bg-rose-100"
                            }`}
                            onClick={() => selectQuotation(quote.quotation_id)}
                            type="button"
                          >
                            Vista rapida
                          </button>
                          <Link
                            className="rounded-lg bg-stone-900 px-3 py-2 text-xs font-black text-white transition hover:bg-stone-700"
                            to={`/quotations/${quote.quotation_id}`}
                          >
                            Detalle
                          </Link>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </MainLayout>
  );
}
