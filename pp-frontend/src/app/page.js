"use client";

import Image from "next/image";
import logo from "./pathways_transparent.png";
import { useState } from "react";
import { TypeAnimation } from "react-type-animation";
import { FaUser, FaRobot } from "react-icons/fa";

export default function Home() {
  const [submitted, setSubmitted] = useState(false);
  const [queryText, setQueryText] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const receiveBotMessage = (text) => {
    setMessages((currentMessages) => [
      ...currentMessages,
      { id: currentMessages.length + 1, text, sender: "bot" },
    ]);
  };

  // Simulate a bot response after user sends a message
  const sendMessage = (text) => {
    return new Promise((resolve) => {
      // Wrap logic in a promise
      const newMessage = { id: messages.length + 1, text, sender: "user" };
      setMessages([...messages, newMessage]);
      setTimeout(() => {
        receiveBotMessage("This is a simulated bot response");
        resolve(); // Resolve the promise after the timeout
      }, 1500); // Simulate a delay for bot response
    });
  };

  const handleInputChange = (e) => {
    setQueryText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!queryText.trim()) return;

    setLoading(true);
    setSubmitted(true);

    await sendMessage(queryText).then(() => {
      setLoading(false); // Ensure loading is set to false after message processing
    });

    setQueryText(""); // Clear input after sending
  };

  return (
    <div className="relative flex min-h-screen flex-col bg-[#212121]">
      <header className="p-2 sticky top-0 z-10 bg-[#212121]">
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

      <div className="flex flex-col flex-grow">
        {/* Chat messages area */}
        <div
          className={`flex-grow overflow-y-auto p-4 ${
            submitted ? "block" : "hidden"
          }`}
        >
          {messages.map((message) => (
            <div
              key={message.id}
              className={`relative max-w-max px-2 py-2 rounded-xl ${
                message.sender === "user" ? "ml-auto" : "mr-auto"
              }`}
            >
              {/* Display message */}
              {message.sender === "user" ? (
                <span className="flex-row flex font-3xl mr-10">
                  {message.text} <FaUser size={40} className="ml-5" />
                </span>
              ) : (
                <span className="flex flex-row font-3xl ml-10">
                  <FaRobot size={40} className="mr-5" />
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
            className="w-full p-5 flex justify-center items-center bg-[#212121] sticky bottom-0"
          >
            <input
              className="shadow appearance-none border rounded p-5 w-11/12 h-12 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="text"
              placeholder="Type your message here..."
              value={queryText}
              onChange={handleInputChange}
              disabled={loading}
            />
            <button
              type="submit"
              className="bg-[#e7b564] text-white rounded px-6 ml-4 h-12"
              disabled={loading}
            >
              Send
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
