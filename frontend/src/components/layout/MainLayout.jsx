import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

export default function MainLayout({ action, children, subtitle, title }) {

    return (

        <div className="min-h-screen bg-[#fff8f3] text-stone-800 lg:flex">

            <Sidebar />

            <div className="min-w-0 flex-1">

                <Navbar action={action} subtitle={subtitle} title={title} />

                <main className="mx-auto w-full max-w-7xl px-5 py-6 sm:px-8 lg:px-10 lg:py-8">

                    {children}

                </main>

            </div>

        </div>
    );
}
