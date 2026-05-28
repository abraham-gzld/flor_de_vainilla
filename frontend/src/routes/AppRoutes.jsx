import { BrowserRouter, Routes, Route } from "react-router-dom";

import Customers from "../pages/Customer";
import CreateQuotation from "../pages/CreateQuotation";
import Dashboard from "../pages/Dashboard";
import QuotationDetail from "../pages/QuotationDetail";
import Quotations from "../pages/Quotations";

export function AppRoutes() {

    return (

        <BrowserRouter>

            <Routes>

                <Route path="/" element={<Dashboard />} />
                <Route path="/customers" element={<Customers />} />
                <Route path="/quotations" element={<Quotations />} />
                <Route path="/quotations/new" element={<CreateQuotation />} />
                <Route path="/quotations/:id" element={<QuotationDetail />} />

            </Routes>

        </BrowserRouter>
    )
}
