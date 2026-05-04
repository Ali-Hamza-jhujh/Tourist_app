import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors());
app.use(bodyParser.json({ limit: "20mb" })); // allow large images

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Chat endpoint
app.post("/chat", async (req, res) => {
  const { message, image, mimeType } = req.body;

  try {
    const content = [];

    if (message && message.trim()) {
      content.push({ type: "text", text: message });
    }

    if (image) {
      content.push({
        type: "image_url",
        image_url: {
          url: `data:${mimeType};base64,${image}`
        }
      });
    }

    // GPT-4o (vision capable)
    const completion = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        {
          role: "user",
          content
        }
      ]
    });

    const reply = completion.choices[0].message.content;
    res.json({ reply });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to process request" });
  }
});

// Optional: reset endpoint
app.post("/reset", (req, res) => {
  // In case you store session/context
  res.json({ status: "reset done" });
});

app.listen(3000, () => console.log("✅ Server running on port 3000"));
