"use client";

import Image from "next/image";
import logo from "./pathways_transparent.png";
import { useState } from "react";
import { TypeAnimation } from "react-type-animation";

export default function Home() {
  const [submitted, setSubmitted] = useState(false);
  const [queryText, setQueryText] = useState("");
  const [messages, setMessages] = useState([]);

  const receiveBotMessage = (text) => {
    setMessages((currentMessages) => [
      ...currentMessages,
      { id: currentMessages.length + 1, text, sender: "bot" },
    ]);
  };

  // Simulate a bot response after user sends a message
  const sendMessage = (text) => {
    const newMessage = { id: messages.length + 1, text, sender: "user" };
    setMessages([...messages, newMessage]);
    setTimeout(() => {
      receiveBotMessage(
        "This is nseThis is a simulated bot responseThis is a simulated bot"
      );
    }, 1500); // Simulate a delay for bot response
  };

  const handleInputChange = (e) => {
    setQueryText(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!queryText.trim()) return;
    setSubmitted(true);
    sendMessage(queryText);
    setQueryText(""); // Clear input after sending
  };

  return (
    <div className="relative flex min-h-screen flex-col bg-[#212121]">
      <header className="p-2">
        <div className="flex items-center">
          <Image src={logo} alt="Pathways logo" width={80} height={60} />
          <span className="text-3xl font-bold text-[#e7b564] ml-3">
            Pathways
          </span>
        </div>
      </header>

      {!submitted && (
        <main className="flex-grow flex items-center justify-center mb-10 transition-all duration-500 ease-in-out">
          <div className="text-center">
            <h1 className="text-7xl font-bold text-[#e7b564] mb-3">
              Course planning, made easy
            </h1>
            <p className="text-xl text-gray-400">
              Welcome to Purdue Pathways, the AI-driven chatbot tailored to
              simplify your course planning at Purdue University.
            </p>
            <p className="text-xl text-gray-400">
              Experience personalized scheduling, course selection, and academic
              advice right at your fingertips.
            </p>

            <form onSubmit={handleSubmit}>
              <input
                className="shadow appearance-none border rounded p-6 w-full text-gray-700 leading-tight focus:outline-none focus:shadow-outline mt-5"
                id="userPrompt"
                type="text"
                placeholder="Ask anything about Purdue courses, scheduling, or planning..."
                value={queryText}
                onChange={(e) => setQueryText(e.target.value)}
              />
            </form>
          </div>
        </main>
      )}

      <div className={`overflow-y-auto p-4 ${submitted ? "block" : "hidden"}`}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`relative max-w-max px-2 py-2 rounded-xl ${
              message.sender === "user" ? "ml-auto" : "mr-auto"
            }`}
          >
            {message.sender === "user" ? (
              <span className="block">{message.text}</span>
            ) : (
              <span className="block">
                <TypeAnimation
                  sequence={[`${message.text}`]}
                  repeat={1}
                  cursor={false}
                />
              </span>
            )}
          </div>
        ))}
      </div>

      {submitted && (
        <form
          onSubmit={handleSubmit}
          className="absolute bottom-0 w-full p-5 flex justify-center items-center mb-5"
        >
          <input
            className="shadow appearance-none border rounded p-5 w-11/12 h-12 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            type="text"
            placeholder="Type your message here..."
            value={queryText}
            onChange={handleInputChange}
          />
          <button
            type="submit"
            className="bg-[#e7b564] text-white rounded px-6 ml-4 h-12"
          >
            Send
          </button>
        </form>
      )}
    </div>
  );
}
