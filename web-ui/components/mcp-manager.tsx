"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Database, Plus, Trash2, Power } from "lucide-react";

interface MCPServer {
  id: string;
  name: string;
  status: "connected" | "disconnected";
  url: string;
}

export function MCPManager() {
  const [servers, setServers] = useState<MCPServer[]>([
    {
      id: "1",
      name: "Demo Server",
      status: "disconnected",
      url: "localhost:3000",
    },
  ]);

  const toggleServerStatus = (id: string) => {
    setServers((prev) =>
      prev.map((server) =>
        server.id === id
          ? {
              ...server,
              status: server.status === "connected" ? "disconnected" : "connected",
            }
          : server
      )
    );
  };

  const removeServer = (id: string) => {
    setServers((prev) => prev.filter((server) => server.id !== id));
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>MCP Servers</CardTitle>
              <CardDescription>
                Manage your Model Context Protocol servers
              </CardDescription>
            </div>
            <Button size="sm" className="gap-2">
              <Plus className="h-4 w-4" />
              Add Server
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {servers.length === 0 ? (
            <div className="text-center py-8">
              <Database className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-sm text-muted-foreground">No servers connected.</p>
              <p className="text-xs text-muted-foreground mt-1">
                Add a server to get started.
              </p>
            </div>
          ) : (
            servers.map((server) => (
              <Card key={server.id} className="border-2">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div
                        className={`h-3 w-3 rounded-full ${
                          server.status === "connected"
                            ? "bg-green-500 animate-pulse"
                            : "bg-gray-400"
                        }`}
                      />
                      <div>
                        <h4 className="font-medium">{server.name}</h4>
                        <p className="text-xs text-muted-foreground">{server.url}</p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant={server.status === "connected" ? "destructive" : "default"}
                        onClick={() => toggleServerStatus(server.id)}
                        className="gap-2"
                      >
                        <Power className="h-3 w-3" />
                        {server.status === "connected" ? "Disconnect" : "Connect"}
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => removeServer(server.id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
}
