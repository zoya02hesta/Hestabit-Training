// import "./globals.css";

// export default function RootLayout({
//   children,
// }: {
//   children: React.ReactNode;
// }) {
//   return (
//     <html lang="en">
//       <body className="bg-gray-100">
//         {children}
//       </body>
//     </html>
//   );
// }



import "./globals.css"

export const metadata = {
  title: "Week 3 Capstone",
  description: "Next.js + Tailwind UI",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
