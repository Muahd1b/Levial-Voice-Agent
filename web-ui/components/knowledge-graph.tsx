"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain, User, Calendar, MapPin, Briefcase } from "lucide-react";

interface KnowledgeItem {
  id: string;
  category: "personal" | "location" | "work" | "schedule";
  key: string;
  value: string;
  icon: React.ReactNode;
}

export function KnowledgeGraph() {
  const knowledgeItems: KnowledgeItem[] = [
    {
      id: "1",
      category: "personal",
      key: "Name",
      value: "Jonas",
      icon: <User className="h-4 w-4" />,
    },
    {
      id: "2",
      category: "location",
      key: "Location",
      value: "Germany",
      icon: <MapPin className="h-4 w-4" />,
    },
    {
      id: "3",
      category: "work",
      key: "Focus",
      value: "AI Development",
      icon: <Briefcase className="h-4 w-4" />,
    },
    {
      id: "4",
      category: "schedule",
      key: "Timezone",
      value: "CET (UTC+1)",
      icon: <Calendar className="h-4 w-4" />,
    },
  ];

  const categoryColors = {
    personal: "bg-blue-500/10 text-blue-600 border-blue-500/20",
    location: "bg-green-500/10 text-green-600 border-green-500/20",
    work: "bg-purple-500/10 text-purple-600 border-purple-500/20",
    schedule: "bg-orange-500/10 text-orange-600 border-orange-500/20",
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-primary" />
            <div>
              <CardTitle>Knowledge Base</CardTitle>
              <CardDescription>
                What the agent knows about you
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          {knowledgeItems.length === 0 ? (
            <div className="text-center py-8">
              <Brain className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-sm text-muted-foreground">Knowledge graph empty.</p>
              <p className="text-xs text-muted-foreground mt-1">
                Start chatting to build your knowledge base.
              </p>
            </div>
          ) : (
            <div className="grid gap-3">
              {knowledgeItems.map((item) => (
                <div
                  key={item.id}
                  className={`p-4 rounded-lg border-2 ${categoryColors[item.category]} transition-all hover:scale-105`}
                >
                  <div className="flex items-center gap-3">
                    <div className="flex-shrink-0">{item.icon}</div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium opacity-70 uppercase tracking-wider">
                        {item.key}
                      </p>
                      <p className="text-sm font-semibold truncate">{item.value}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card className="bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <Brain className="h-5 w-5 text-primary mt-0.5" />
            <div className="space-y-1">
              <p className="text-sm font-medium">Adaptive Learning</p>
              <p className="text-xs text-muted-foreground">
                The agent learns from your conversations and adapts to your preferences over time.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
