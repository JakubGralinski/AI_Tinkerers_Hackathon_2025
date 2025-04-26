import { NextResponse } from "next/server";

// Route handler for the /api/python/process endpoint
export async function POST(req: Request) {
    try {
        const body = await req.json();
        const endpoint = req.url.endsWith("/process") ? "process" : "analyze";

        const response = await fetch(`http://localhost:5000/api/python/${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            throw new Error(`Error from Python API: ${response.statusText}`);
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error: any) {
        console.error(`Error in /api/python/${req.url.endsWith("/process") ? "process" : "analyze"}:`, error);
        return NextResponse.json(
            { error: error.message || "Internal Server Error" },
            { status: 500 }
        );
    }
} 