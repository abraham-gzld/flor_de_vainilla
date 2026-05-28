import api from "./api";

export async function getQuotations() {
  const response = await api.get("/quotations/");
  return response.data;
}

export async function getFullQuotation(id) {
  const response = await api.get(`/quotations/${id}/full`);
  return response.data;
}

export async function createQuotation(quotation) {
  const response = await api.post("/quotations/", quotation);
  return response.data;
}

export async function approveQuotation(id) {
  const response = await api.put(`/quotations/${id}/approve`);
  return response.data;
}

export async function cancelQuotation(id) {
  const response = await api.put(`/quotations/${id}/cancel`);
  return response.data;
}

export async function createDetailQuotation(detail) {
  const response = await api.post("/detail-quotations/", detail);
  return response.data;
}

export async function createCustomCake(cake) {
  const response = await api.post("/custom-cakes/", cake);
  return response.data;
}

export async function addCakeExtra(extra) {
  const response = await api.post("/cake-extras/", extra);
  return response.data;
}
