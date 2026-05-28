import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";

import MainLayout from "../components/layout/MainLayout";
import {
  approveQuotation,
  cancelQuotation,
  getFullQuotation,
} from "../services/quotationService";
import { formatCurrency, formatDate, statusLabel } from "../utils/formatters";

function detailTitle(detail) {
  if (detail.product_type === "simple_product") {
    return detail.product?.name || "Producto eliminado";
  }

  return detail.custom_cake?.description || "Pastel personalizado";
}

function detailDescription(detail) {
  const cake = detail.custom_cake;

  if (!cake) {
    return detail.comment || "Sin comentario";
  }

  return [
    cake.size?.name,
    cake.flavor?.name,
    cake.filling?.name,
    cake.decoration?.name,
  ]
    .filter(Boolean)
    .join(" · ");
}

export default function QuotationDetail() {
  const { id } = useParams();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [quotation, setQuotation] = useState(null);

  useEffect(() => {
    let ignore = false;

    getFullQuotation(id)
      .then((data) => {
        if (!ignore) {
          setQuotation(data);
        }
      })
      .catch(() => {
        if (!ignore) {
          setError("No se pudo cargar el detalle de la cotizacion.");
        }
      })
      .finally(() => {
        if (!ignore) {
          setLoading(false);
        }
      });

    return () => {
      ignore = true;
    };
  }, [id]);

  const extras = useMemo(
    () =>
      quotation?.details?.flatMap((detail) => detail.custom_cake?.extras || []) || [],
    [quotation]
  );

  async function updateStatus(action) {
    try {
      if (action === "approve") {
        await approveQuotation(id);
      } else {
        await cancelQuotation(id);
      }

      setQuotation(await getFullQuotation(id));
    } catch {
      setError("No se pudo actualizar el estado.");
    }
  }

  return (
    <MainLayout
      subtitle={
        quotation
          ? `Cotizacion #${quotation.quotation_id} · ${formatDate(quotation.quotation_date)}`
          : "Detalle desde la base de datos"
      }
      title="Detalle de cotizacion"
    >
      {error && (
        <div className="mb-6 rounded-2xl bg-red-50 p-4 text-sm font-bold text-red-700 ring-1 ring-red-100">
          {error}
        </div>
      )}

      {loading && (
        <div className="rounded-2xl bg-white p-6 font-bold text-stone-500 shadow-sm ring-1 ring-rose-100">
          Cargando cotizacion...
        </div>
      )}

      {!loading && quotation && (
        <section className="grid gap-6 lg:grid-cols-[1fr_360px]">
          <article className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
            <Link className="text-sm font-bold text-rose-600 hover:text-rose-700" to="/quotations">
              Volver a cotizaciones
            </Link>

            <div className="mt-5 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h1 className="text-3xl font-black text-stone-900">
                  Cotizacion #{quotation.quotation_id}
                </h1>
                <p className="mt-1 text-stone-500">
                  Cliente: {quotation.customer?.name || "Cliente no disponible"}
                </p>
                <p className="text-sm text-stone-500">
                  {quotation.customer?.phone || "Sin telefono"}
                </p>
              </div>
              <span className="rounded-full bg-rose-50 px-4 py-2 text-sm font-black text-rose-700">
                {statusLabel(quotation.status)}
              </span>
            </div>

            <div className="mt-6 grid gap-4 sm:grid-cols-3">
              <div className="rounded-xl bg-[#fff8f3] p-4">
                <p className="text-xs font-bold uppercase text-stone-400">Fecha</p>
                <p className="mt-2 font-black text-stone-800">
                  {formatDate(quotation.quotation_date)}
                </p>
              </div>
              <div className="rounded-xl bg-[#fff8f3] p-4">
                <p className="text-xs font-bold uppercase text-stone-400">Partidas</p>
                <p className="mt-2 font-black text-stone-800">
                  {quotation.details?.length || 0}
                </p>
              </div>
              <div className="rounded-xl bg-[#fff8f3] p-4">
                <p className="text-xs font-bold uppercase text-stone-400">Extras</p>
                <p className="mt-2 font-black text-stone-800">{extras.length}</p>
              </div>
            </div>

            {quotation.note && (
              <div className="mt-6 rounded-2xl bg-rose-50 p-4 text-sm text-stone-600">
                {quotation.note}
              </div>
            )}

            <div className="mt-6 rounded-2xl ring-1 ring-rose-100">
              {quotation.details?.length === 0 && (
                <div className="px-5 py-6 text-center font-bold text-stone-500">
                  Esta cotizacion no tiene partidas.
                </div>
              )}

              {quotation.details?.map((detail) => (
                <div
                  className="border-b border-rose-100 px-5 py-4 last:border-b-0"
                  key={detail.detail_id}
                >
                  <div className="flex justify-between gap-4">
                    <div>
                      <p className="font-bold text-stone-700">{detailTitle(detail)}</p>
                      <p className="mt-1 text-sm text-stone-500">
                        {detailDescription(detail)}
                      </p>
                      <p className="mt-1 text-xs font-bold uppercase text-stone-400">
                        Cantidad: {detail.quantity}
                      </p>
                    </div>
                    <span className="font-black text-stone-900">
                      {formatCurrency(detail.subtotal)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </article>

          <aside className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100">
            <p className="text-sm font-bold uppercase text-rose-400">Total</p>
            <p className="mt-4 text-5xl font-black text-stone-900">
              {formatCurrency(quotation.total)}
            </p>
            <p className="mt-3 text-sm leading-6 text-stone-500">
              Total calculado desde detail_quotation y custom_cake.
            </p>

            <div className="mt-6 grid gap-3">
              <button
                className="rounded-xl bg-rose-500 px-5 py-3 text-sm font-black text-white shadow-sm transition hover:bg-rose-600"
                onClick={() => updateStatus("approve")}
                type="button"
              >
                Aprobar cotizacion
              </button>
              <button
                className="rounded-xl bg-[#fff8f3] px-5 py-3 text-sm font-black text-stone-700 ring-1 ring-rose-100 transition hover:bg-rose-50"
                onClick={() => updateStatus("cancel")}
                type="button"
              >
                Cancelar
              </button>
            </div>
          </aside>
        </section>
      )}
    </MainLayout>
  );
}
