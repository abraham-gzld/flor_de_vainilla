import api from "./api";

export async function getProducts() {
  const response = await api.get("/products/");
  return response.data;
}

export async function getSizes() {
  const response = await api.get("/sizes/");
  return response.data;
}

export async function getFlavors() {
  const response = await api.get("/flavors/");
  return response.data;
}

export async function getFillings() {
  const response = await api.get("/fillings/");
  return response.data;
}

export async function getDecorations() {
  const response = await api.get("/decorations/");
  return response.data;
}

export async function getExtras() {
  const response = await api.get("/extras/");
  return response.data;
}
