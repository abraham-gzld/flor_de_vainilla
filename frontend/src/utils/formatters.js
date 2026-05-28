export function formatCurrency(value) {
  return new Intl.NumberFormat("es-MX", {
    currency: "MXN",
    maximumFractionDigits: 0,
    style: "currency",
  }).format(Number(value || 0));
}

export function formatDate(value) {
  if (!value) {
    return "Sin fecha";
  }

  return new Intl.DateTimeFormat("es-MX", {
    day: "2-digit",
    month: "short",
  }).format(new Date(value));
}

export function statusLabel(status) {
  const labels = {
    approved: "Aprobada",
    canceled: "Cancelada",
    pending: "Pendiente",
  };

  return labels[status] || status || "Pendiente";
}

export function quotationDetailTitle(detail) {
  if (detail?.product_type === "simple_product") {
    return detail.product?.name || "Producto eliminado";
  }

  return detail?.custom_cake?.description || "Pastel personalizado";
}

export function quotationDetailDescription(detail) {
  const cake = detail?.custom_cake;

  if (!cake) {
    return detail?.comment || "Sin comentario";
  }

  return [
    cake.size?.name,
    cake.flavor?.name,
    cake.filling?.name,
    cake.decoration?.name,
  ]
    .filter(Boolean)
    .join(" / ");
}
