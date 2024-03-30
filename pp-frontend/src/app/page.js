import Image from "next/image";
import logo from "./pathways_transparent.png";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-[#212121]">
      <header className="p-2">
        <div className="flex items-center">
          <Image src={logo} alt="Pathways logo" width={80} height={60} />
          <span className="text-3xl font-bold text-[#e7b564] ml-3">
            Pathways
          </span>
        </div>
      </header>
      <main className="flex-grow flex items-center justify-center mb-10">
        <div className="text-center mb-30">
          <h1 className="text-7xl font-bold text-[#e7b564] mb-3">
            Course planning, made easy
          </h1>
          <p className="text-xl text-gray-400">
            Welcome to Purdue Pathways, the AI-driven chatbot tailored to
            simplify your course planning at Purdue University.
          </p>
          <p className="text-xl text-gray-400">
            {" "}
            Experience personalized scheduling, course selection, and academic
            advice right at your fingertips.
          </p>

          <input
            class="shadow appearance-none border rounded p-6 w-full text-gray-700 leading-tight focus:outline-none focus:shadow-outline mt-5"
            id="userPrompt"
            type="text"
            placeholder="let's forward your education..."
          />
        </div>
      </main>
    </div>
  );
}
