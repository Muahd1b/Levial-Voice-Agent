import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { motion } from "framer-motion";
import { Brain, User, Heart, Pencil, Save, X, Plus, Trash2 } from "lucide-react";

interface KnowledgeGraphProps {
  userProfile?: any;
  onUpdate?: (updates: any) => void;
}

export function KnowledgeGraph({ userProfile, onUpdate }: KnowledgeGraphProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState<any>(null);

  // Use real profile data or fallback to demo data
  const profile = userProfile || {
    name: "User",
    interests: [],
    facts: {},
    preferences: {}
  };

  const startEditing = () => {
    setEditData(JSON.parse(JSON.stringify(profile))); // Deep copy
    setIsEditing(true);
  };

  const cancelEditing = () => {
    setIsEditing(false);
    setEditData(null);
  };

  const saveEditing = () => {
    if (onUpdate) {
      onUpdate(editData);
    }
    setIsEditing(false);
  };

  const updateField = (category: string, key: string, value: string) => {
    if (!editData) return;
    
    if (category === "personal") {
      setEditData({ ...editData, [key]: value });
    } else if (category === "facts") {
      setEditData({ ...editData, facts: { ...editData.facts, [key]: value } });
    }
  };

  const updateInterest = (index: number, value: string) => {
    if (!editData) return;
    const newInterests = [...editData.interests];
    newInterests[index] = value;
    setEditData({ ...editData, interests: newInterests });
  };

  const addInterest = () => {
    if (!editData) return;
    setEditData({ ...editData, interests: [...editData.interests, ""] });
  };

  const removeInterest = (index: number) => {
    if (!editData) return;
    const newInterests = [...editData.interests];
    newInterests.splice(index, 1);
    setEditData({ ...editData, interests: newInterests });
  };

  const removeFact = (key: string) => {
    if (!editData) return;
    const newFacts = { ...editData.facts };
    delete newFacts[key];
    setEditData({ ...editData, facts: newFacts });
  };

  // Display data (either current profile or editData if editing)
  const displayData = isEditing ? editData : profile;

  const knowledgeItems = [
    {
      category: "Personal",
      icon: User,
      color: "bg-blue-500/10 text-blue-500",
      items: [
        { label: "Name", value: displayData.name, key: "name", editable: true }
      ]
    },
    {
      category: "Interests",
      icon: Heart,
      color: "bg-pink-500/10 text-pink-500",
      items: displayData.interests?.map((interest: string, i: number) => ({
        label: `Interest ${i + 1}`,
        value: interest,
        index: i,
        isList: true
      })) || []
    },
    {
      category: "Facts",
      icon: Brain,
      color: "bg-purple-500/10 text-purple-500",
      items: Object.entries(displayData.facts || {}).map(([key, value]) => ({
        label: key,
        value: value as string,
        key: key,
        isFact: true
      }))
    }
  ];

  return (
    <div className="space-y-6">
      <Card className="bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Brain className="h-5 w-5" />
              My Knowledge About You
            </CardTitle>
            <CardDescription>
              Information learned from our conversations
            </CardDescription>
          </div>
          <div>
            {!isEditing ? (
              <Button variant="outline" size="sm" onClick={startEditing} className="gap-2">
                <Pencil className="h-4 w-4" /> Edit
              </Button>
            ) : (
              <div className="flex gap-2">
                <Button variant="ghost" size="sm" onClick={cancelEditing}>
                  <X className="h-4 w-4" /> Cancel
                </Button>
                <Button size="sm" onClick={saveEditing}>
                  <Save className="h-4 w-4" /> Save
                </Button>
              </div>
            )}
          </div>
        </CardHeader>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {knowledgeItems.map((category, idx) => (
          <motion.div
            key={category.category}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <Card className="hover:shadow-lg transition-shadow h-full">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className={`p-2 rounded-lg ${category.color}`}>
                      <category.icon className="h-4 w-4" />
                    </div>
                    <CardTitle className="text-lg">{category.category}</CardTitle>
                  </div>
                  {isEditing && category.category === "Interests" && (
                    <Button variant="ghost" size="icon" className="h-6 w-6" onClick={addInterest}>
                      <Plus className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {category.items.length > 0 ? (
                  <div className="space-y-2">
                    {category.items.map((item: any, i: number) => (
                      <motion.div
                        key={i}
                        className="p-2 rounded-md bg-muted/50 hover:bg-muted transition-colors"
                      >
                        <p className="text-xs text-muted-foreground capitalize mb-1">{item.label}</p>
                        {isEditing ? (
                          <div className="flex gap-2">
                            <Input 
                              value={item.value} 
                              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                                if (item.isList) updateInterest(item.index, e.target.value);
                                else if (item.isFact) updateField("facts", item.key, e.target.value);
                                else updateField("personal", item.key, e.target.value);
                              }}
                              className="h-8 text-sm"
                            />
                            {(item.isList || item.isFact) && (
                              <Button 
                                variant="ghost" 
                                size="icon" 
                                className="h-8 w-8 text-destructive hover:text-destructive"
                                onClick={() => {
                                  if (item.isList) removeInterest(item.index);
                                  if (item.isFact) removeFact(item.key);
                                }}
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            )}
                          </div>
                        ) : (
                          <p className="text-sm font-medium">{item.value}</p>
                        )}
                      </motion.div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-4">
                    <p className="text-sm text-muted-foreground italic mb-2">
                      No {category.category.toLowerCase()} learned yet
                    </p>
                    {isEditing && category.category === "Interests" && (
                      <Button variant="outline" size="sm" onClick={addInterest}>
                        Add Interest
                      </Button>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <Card className="bg-muted/30">
        <CardContent className="pt-6">
          <p className="text-sm text-muted-foreground text-center">
            💡 I learn about you from our conversations, but you can also edit this knowledge manually.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
