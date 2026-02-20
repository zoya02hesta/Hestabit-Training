"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import Link from "next/link";

export default function LandingContent() {
  return (
    <div className="bg-gray-50 text-gray-800">

      {/* HERO */}
      <section className="container mx-auto px-6 py-24 flex flex-col md:flex-row items-center gap-12">

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex-1 space-y-6 text-center md:text-left"
        >
          <h1 className="text-4xl md:text-5xl font-bold leading-tight">
            Build Modern Dashboards Faster
          </h1>

          <p className="text-gray-500 text-lg">
            Purity UI helps teams build beautiful, responsive dashboards with
            Next.js and Tailwind CSS.
          </p>

          <div className="space-x-4">
            <Link
              href="/dashboard"
              className="px-6 py-3 bg-blue-600 text-white rounded-xl shadow hover:bg-blue-700 transition"
            >
              Get Started
            </Link>

            <Link
              href="/about"
              className="px-6 py-3 border border-gray-300 rounded-xl hover:bg-gray-100 transition"
            >
              Learn More
            </Link>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="flex-1"
        >
          <Image
            src="https://images.unsplash.com/photo-1551288049-bebda4e38f71"
            alt="Dashboard preview"
            width={600}
            height={400}
            className="rounded-2xl shadow-lg"
            priority
          />
        </motion.div>
      </section>

      {/* FEATURES */}
      <section className="container mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">
          Powerful Features
        </h2>

        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              title: "Optimized Performance",
              desc: "Built with Next.js image optimization and server rendering.",
            },
            {
              title: "Responsive Design",
              desc: "Fully responsive layout built with Tailwind CSS utilities.",
            },
            {
              title: "Clean Architecture",
              desc: "Nested layouts and scalable folder structure.",
            },
          ].map((feature, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.05 }}
              className="bg-white p-8 rounded-2xl shadow-sm border"
            >
              <h3 className="font-semibold text-lg mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-500 text-sm">
                {feature.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* TESTIMONIALS */}
<section className="bg-gray-100 py-20">
  <div className="container mx-auto px-6">

    <h2 className="text-3xl font-bold text-center mb-12">
      What Our Users Say
    </h2>

    {/** Testimonials Data */}
    {(() => {
      const testimonials = [
        {
          id: 1,
          name: "Prince Keller",
          role: "Product Manager",
          comment:
            "This dashboard template saved our team weeks of development time and improved productivity significantly.",
        },
        {
          id: 2,
          name: "Sara Williams",
          role: "UI/UX Designer",
          comment:
            "The clean architecture and beautiful UI components made development smooth and enjoyable.",
        },
        {
          id: 3,
          name: "Daniel Kim",
          role: "Software Engineer",
          comment:
            "Using Next.js image optimization and responsive design helped us achieve top performance scores.",
        },
      ];

      return (
        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((user) => (
            <motion.div
              key={user.id}
              whileHover={{ y: -6 }}
              transition={{ type: "spring", stiffness: 200 }}
              className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition"
            >
              <div className="flex items-center gap-4 mb-4">
                <Image
                  src={`https://i.pravatar.cc/50?img=${user.id}`}
                  alt={user.name}
                  width={50}
                  height={50}
                  className="rounded-full"
                />
                <div>
                  <p className="font-semibold text-gray-800">
                    {user.name}
                  </p>
                  <p className="text-gray-400 text-sm">
                    {user.role}
                  </p>
                </div>
              </div>

              <p className="text-gray-500 text-sm leading-relaxed">
                "{user.comment}"
              </p>
            </motion.div>
          ))}
        </div>
      );
    })()}

  </div>
</section>


      {/* FOOTER */}
      <footer className="bg-white border-t py-8">
        <div className="container mx-auto px-6 text-center text-gray-500 text-sm">
          © {new Date().getFullYear()} Purity Dashboard. Made By Zoya Fatima
        </div>
      </footer>

    </div>
  );
}
