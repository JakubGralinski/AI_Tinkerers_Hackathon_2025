import { NextResponse } from "next/server";

export async function POST(req: Request) {
    try {
        const body = await req.json();

        const response = await fetch("http://localhost:5000/api/python/process", {
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
        console.error("Error in /api/python/process:", error);
        return NextResponse.json(
            { error: error.message || "Internal Server Error" },
            { status: 500 }
        );
    }
} 