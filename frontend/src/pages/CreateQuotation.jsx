import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import MainLayout from "../components/layout/MainLayout";
import {
  getDecorations,
  getExtras,
  getFillings,
  getFlavors,
  getProducts,
  getSizes,
} from "../services/catalogService";
import { getCustomers } from "../services/customerService";
import {
  addCakeExtra,
  createCustomCake,
  createDetailQuotation,
  createQuotation,
} from "../services/quotationService";
import { formatCurrency } from "../utils/formatters";

const baseCakePrice = 500;

const emptyForm = {
  comment: "",
  customer_id: "",
  decoration_id: "",
  description: "",
  extra_ids: [],
  filling_id: "",
  flavor_id: "",
  note: "",
  product_id: "",
  product_type: "simple_product",
  quantity: 1,
  servings: "",
  size_id: "",
};

function SelectField({ children, label, ...props }) {
  return (
    <label className="grid gap-2">
      <span className="text-sm font-bold text-stone-700">{label}</span>
      <select
        className="h-12 rounded-xl border border-rose-100 bg-[#fff8f3] px-4 text-sm outline-none transition focus:border-rose-300 focus:bg-white focus:ring-4 focus:ring-rose-100"
        {...props}
      >
        {children}
      </select>
    </label>
  );
}

export default function CreateQuotation() {
  const navigate = useNavigate();
  const [catalog, setCatalog] = useState({
    customers: [],
    decorations: [],
    extras: [],
    fillings: [],
    flavors: [],
    products: [],
    sizes: [],
  });
  const [error, setError] = useState("");
  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    let ignore = false;

    async function loadCatalog() {
      try {
        const [
          customers,
          products,
          sizes,
          flavors,
          fillings,
          decorations,
          extras,
        ] = await Promise.all([
          getCustomers(),
          getProducts(),
          getSizes(),
          getFlavors(),
          getFillings(),
          getDecorations(),
          getExtras(),
        ]);

        if (!ignore) {
          setCatalog({
            customers,
            decorations,
            extras,
            fillings,
            flavors,
            products: products.filter((product) => product.active),
            sizes,
          });
        }
      } catch {
        if (!ignore) {
          setError("No se pudo cargar el catalogo desde la base de datos.");
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    loadCatalog();

    return () => {
      ignore = true;
    };
  }, []);

  const selectedProduct = useMemo(
    () =>
      catalog.products.find(
        (product) => product.product_id === Number(form.product_id)
      ),
    [catalog.products, form.product_id]
  );

  const customParts = useMemo(
    () => [
      catalog.sizes.find((item) => item.size_id === Number(form.size_id)),
      catalog.flavors.find((item) => item.flavor_id === Number(form.flavor_id)),
      catalog.fillings.find((item) => item.filling_id === Number(form.filling_id)),
      catalog.decorations.find(
        (item) => item.decoration_id === Number(form.decoration_id)
      ),
      ...catalog.extras.filter((item) => form.extra_ids.includes(String(item.extra_id))),
    ],
    [catalog, form]
  );

  const quantity = Math.max(Number(form.quantity) || 1, 1);

  const estimatedUnitPrice =
    form.product_type === "simple_product"
      ? Number(selectedProduct?.base_price || 0)
      : customParts.reduce(
          (total, item) => total + Number(item?.price_extra || 0),
          baseCakePrice
        );

  const estimatedTotal = estimatedUnitPrice * quantity;

  function updateField(field, value) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  function toggleExtra(extraId) {
    setForm((current) => {
      const nextExtras = current.extra_ids.includes(extraId)
        ? current.extra_ids.filter((id) => id !== extraId)
        : [...current.extra_ids, extraId];

      return {
        ...current,
        extra_ids: nextExtras,
      };
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    if (!form.customer_id) {
      setError("Selecciona un cliente.");
      return;
    }

    if (form.product_type === "simple_product" && !form.product_id) {
      setError("Selecciona un producto.");
      return;
    }

    if (
      form.product_type === "custom_cake" &&
      (!form.size_id || !form.flavor_id || !form.filling_id || !form.decoration_id)
    ) {
      setError("Completa tamano, sabor, relleno y decoracion.");
      return;
    }

    try {
      setSaving(true);

      const quotation = await createQuotation({
        customer_id: Number(form.customer_id),
        note: form.note || null,
        status: "pending",
        subtotal: 0,
        total: 0,
      });

      const detail = await createDetailQuotation({
        comment: form.comment || null,
        product_id:
          form.product_type === "simple_product" ? Number(form.product_id) : null,
        product_type: form.product_type,
        quantity,
        quotation_id: quotation.quotation_id,
        subtotal: form.product_type === "simple_product" ? estimatedTotal : 0,
        unit_price: form.product_type === "simple_product" ? estimatedUnitPrice : 0,
      });

      if (form.product_type === "custom_cake") {
        const cake = await createCustomCake({
          decoration_id: Number(form.decoration_id),
          description: form.description || null,
          detail_id: detail.detail_id,
          filling_id: Number(form.filling_id),
          flavor_id: Number(form.flavor_id),
          servings: form.servings ? Number(form.servings) : null,
          size_id: Number(form.size_id),
        });

        for (const extraId of form.extra_ids) {
          await addCakeExtra({
            cake_id: cake.cake_id,
            extra_id: Number(extraId),
          });
        }
      }

      navigate(`/quotations/${quotation.quotation_id}`);
    } catch {
      setError("No se pudo guardar la cotizacion.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <MainLayout
      subtitle="Crea cotizaciones usando clientes, productos y catalogos de la BDD"
      title="Nueva cotizacion"
    >
      <section className="grid gap-6 lg:grid-cols-[1fr_360px]">
        <form
          className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-rose-100"
          onSubmit={handleSubmit}
        >
          <h1 className="text-3xl font-black text-stone-900">Datos del pedido</h1>
          <p className="mt-1 text-sm text-stone-500">
            La cotizacion se guarda en quotation, detail_quotation y custom_cake.
          </p>

          {error && (
            <div className="mt-6 rounded-2xl bg-red-50 p-4 text-sm font-bold text-red-700 ring-1 ring-red-100">
              {error}
            </div>
          )}

          <div className="mt-6 grid gap-5 sm:grid-cols-2">
            <SelectField
              disabled={loading}
              label="Cliente"
              onChange={(event) => updateField("customer_id", event.target.value)}
              value={form.customer_id}
            >
              <option value="">Selecciona cliente</option>
              {catalog.customers.map((customer) => (
                <option key={customer.customer_id} value={customer.customer_id}>
                  {customer.name}
                </option>
              ))}
            </SelectField>

            <SelectField
              label="Tipo"
              onChange={(event) => updateField("product_type", event.target.value)}
              value={form.product_type}
            >
              <option value="simple_product">Producto simple</option>
              <option value="custom_cake">Pastel personalizado</option>
            </SelectField>

            <label className="grid gap-2">
              <span className="text-sm font-bold text-stone-700">Cantidad</span>
              <input
                className="h-12 rounded-xl border border-rose-100 bg-[#fff8f3] px-4 text-sm outline-none transition focus:border-rose-300 focus:bg-white focus:ring-4 focus:ring-rose-100"
                min="1"
                onChange={(event) => updateField("quantity", event.target.value)}
                type="number"
                value={form.quantity}
              />
            </label>

            {form.product_type === "simple_product" && (
              <SelectField
                disabled={loading}
                label="Producto"
                onChange={(event) => updateField("product_id", event.target.value)}
                value={form.product_id}
              >
                <option value="">Selecciona producto</option>
                {catalog.products.map((product) => (
                  <option key={product.product_id} value={product.product_id}>
                    {product.name} · {formatCurrency(product.base_price)}
                  </option>
                ))}
              </SelectField>
            )}

            {form.product_type === "custom_cake" && (
              <>
                <SelectField
                  disabled={loading}
                  label="Tamano"
                  onChange={(event) => updateField("size_id", event.target.value)}
                  value={form.size_id}
                >
                  <option value="">Selecciona tamano</option>
                  {catalog.sizes.map((size) => (
                    <option key={size.size_id} value={size.size_id}>
                      {size.name} · +{formatCurrency(size.price_extra)}
                    </option>
                  ))}
                </SelectField>

                <SelectField
                  disabled={loading}
                  label="Sabor"
                  onChange={(event) => updateField("flavor_id", event.target.value)}
                  value={form.flavor_id}
                >
                  <option value="">Selecciona sabor</option>
                  {catalog.flavors.map((flavor) => (
                    <option key={flavor.flavor_id} value={flavor.flavor_id}>
                      {flavor.name} · +{formatCurrency(flavor.price_extra)}
                    </option>
                  ))}
                </SelectField>

                <SelectField
                  disabled={loading}
                  label="Relleno"
                  onChange={(event) => updateField("filling_id", event.target.value)}
                  value={form.filling_id}
                >
                  <option value="">Selecciona relleno</option>
                  {catalog.fillings.map((filling) => (
                    <option key={filling.filling_id} value={filling.filling_id}>
                      {filling.name} · +{formatCurrency(filling.price_extra)}
                    </option>
                  ))}
                </SelectField>

                <SelectField
                  disabled={loading}
                  label="Decoracion"
                  onChange={(event) => updateField("decoration_id", event.target.value)}
                  value={form.decoration_id}
                >
                  <option value="">Selecciona decoracion</option>
                  {catalog.decorations.map((decoration) => (
                    <option key={decoration.decoration_id} value={decoration.decoration_id}>
                      {decoration.name} · +{formatCurrency(decoration.price_extra)}
                    </option>
                  ))}
                </SelectField>

                <label className="grid gap-2">
                  <span className="text-sm font-bold text-stone-700">Porciones</span>
                  <input
                    className="h-12 rounded-xl border border-rose-100 bg-[#fff8f3] px-4 text-sm outline-none transition focus:border-rose-300 focus:bg-white focus:ring-4 focus:ring-rose-100"
                    min="1"
                    onChange={(event) => updateField("servings", event.target.value)}
                    type="number"
                    value={form.servings}
                  />
                </label>
              </>
            )}
          </div>

          {form.product_type === "custom_cake" && (
            <div className="mt-5 rounded-2xl bg-[#fff8f3] p-4">
              <p className="text-sm font-bold text-stone-700">Extras</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {catalog.extras.length === 0 && (
                  <p className="text-sm font-bold text-stone-500">
                    No hay extras registrados.
                  </p>
                )}

                {catalog.extras.map((extra) => (
                  <label
                    className="flex items-center gap-2 rounded-xl bg-white px-3 py-2 text-sm font-bold text-stone-600 ring-1 ring-rose-100"
                    key={extra.extra_id}
                  >
                    <input
                      checked={form.extra_ids.includes(String(extra.extra_id))}
                      onChange={() => toggleExtra(String(extra.extra_id))}
                      type="checkbox"
                    />
                    {extra.name} · +{formatCurrency(extra.price_extra)}
                  </label>
                ))}
              </div>
            </div>
          )}

          <label className="mt-5 grid gap-2">
            <span className="text-sm font-bold text-stone-700">Descripcion</span>
            <textarea
              className="min-h-28 rounded-xl border border-rose-100 bg-[#fff8f3] px-4 py-3 text-sm outline-none transition placeholder:text-stone-400 focus:border-rose-300 focus:bg-white focus:ring-4 focus:ring-rose-100"
              onChange={(event) => updateField("description", event.target.value)}
              placeholder="Colores, relleno, dedicatoria, referencias..."
              value={form.description}
            />
          </label>

          <label className="mt-5 grid gap-2">
            <span className="text-sm font-bold text-stone-700">Nota interna</span>
            <textarea
              className="min-h-24 rounded-xl border border-rose-100 bg-[#fff8f3] px-4 py-3 text-sm outline-none transition placeholder:text-stone-400 focus:border-rose-300 focus:bg-white focus:ring-4 focus:ring-rose-100"
              onChange={(event) => updateField("note", event.target.value)}
              placeholder="Notas para la cotizacion..."
              value={form.note}
            />
          </label>

          <div className="mt-6 flex flex-wrap justify-end gap-3">
            <button
              className="rounded-xl bg-white px-5 py-3 text-sm font-black text-stone-700 ring-1 ring-rose-100 transition hover:bg-rose-50 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={saving}
              onClick={() => setForm(emptyForm)}
              type="button"
            >
              Limpiar
            </button>
            <button
              className="rounded-xl bg-rose-500 px-5 py-3 text-sm font-black text-white shadow-sm transition hover:bg-rose-600 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={saving || loading}
              type="submit"
            >
              {saving ? "Guardando..." : "Guardar cotizacion"}
            </button>
          </div>
        </form>

        <aside className="rounded-2xl bg-[#3b2a28] p-6 text-white shadow-sm">
          <p className="text-sm font-bold uppercase text-rose-200">Resumen</p>
          <p className="mt-5 text-4xl font-black">{formatCurrency(estimatedTotal)}</p>
          <p className="mt-2 text-sm leading-6 text-rose-50/80">
            Estimado segun catalogos. El backend guarda el total final.
          </p>

          <div className="mt-6 space-y-3 text-sm">
            <div className="flex justify-between border-b border-white/10 pb-3">
              <span>Precio unitario</span>
              <span>{formatCurrency(estimatedUnitPrice)}</span>
            </div>
            <div className="flex justify-between border-b border-white/10 pb-3">
              <span>Cantidad</span>
              <span>{quantity}</span>
            </div>
            <div className="flex justify-between">
              <span>Total</span>
              <span>{formatCurrency(estimatedTotal)}</span>
            </div>
          </div>
        </aside>
      </section>
    </MainLayout>
  );
}
