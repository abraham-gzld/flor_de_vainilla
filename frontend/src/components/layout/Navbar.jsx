export default function Navbar({
    action,
    subtitle = "Control de pedidos, clientes y cotizaciones",
    title = "Dashboard",
}) {

    return (

        <header className="sticky top-0 z-10 border-b border-rose-100 bg-white/85 px-5 py-4 shadow-sm backdrop-blur sm:px-8 lg:px-10">

            <div className="mx-auto flex w-full max-w-7xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                <div>

                    <p className="text-xs font-bold uppercase text-rose-400">
                        Flor de Vainilla
                    </p>

                    <h2 className="mt-1 text-2xl font-black text-stone-800">
                        {title}
                    </h2>

                    <p className="text-sm text-stone-500">
                        {subtitle}
                    </p>

                </div>

                <div className="flex items-center gap-3">

                    {action}

                    <div className="grid h-11 w-11 place-items-center rounded-xl bg-rose-100 text-sm font-black text-rose-600 ring-1 ring-rose-200">
                        FV
                    </div>

                </div>

            </div>

        </header>
    );
}
