
import React from 'react';
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Github, Linkedin, Star, Trophy } from 'lucide-react';

export function PortfolioView({ projects, userProfile }) {
  const { toast } = useToast();
  
  const completedProjects = projects.filter(p => p.status === 'completed');

  const exportPortfolio = () => {
    toast({
      title: "🚧 This feature isn't implemented yet—but don't worry! You can request it in your next prompt! 🚀"
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-white">Portfolio Showcase</h2>
        <Button onClick={exportPortfolio} className="bg-gradient-to-r from-purple-500 to-blue-500">
          Export Portfolio
        </Button>
      </div>

      <Card className="bg-white/10 backdrop-blur-lg border-white/20">
        <CardContent className="p-8">
          <div className="text-center mb-8">
            <Avatar className="h-24 w-24 mx-auto mb-4 border-4 border-purple-400">
              <AvatarImage src={userProfile.avatar} />
              <AvatarFallback className="bg-gradient-to-r from-purple-500 to-blue-500 text-white text-2xl">
                {userProfile.name.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <h3 className="text-2xl font-bold text-white mb-2">{userProfile.name}</h3>
            <p className="text-purple-200 mb-4">{userProfile.bio}</p>
            <div className="flex justify-center space-x-4">
              <Button variant="outline" size="sm" className="border-white/20 text-white">
                <Github className="h-4 w-4 mr-2" />
                GitHub
              </Button>
              <Button variant="outline" size="sm" className="border-white/20 text-white">
                <Linkedin className="h-4 w-4 mr-2" />
                LinkedIn
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {completedProjects.map((project) => (
              <div key={project.id} className="bg-white/5 rounded-lg p-4 border border-white/10">
                <h4 className="text-white font-semibold mb-2">{project.name}</h4>
                <p className="text-purple-200 text-sm mb-3">{project.description}</p>
                <div className="flex justify-between items-center">
                  <Badge className="bg-purple-500 text-white">{project.technology}</Badge>
                  <div className="flex space-x-2">
                    <Button size="sm" variant="ghost" className="text-white hover:bg-white/10">
                      <Github className="h-3 w-3" />
                    </Button>
                    <Button size="sm" variant="ghost" className="text-white hover:bg-white/10">
                      <Star className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {completedProjects.length === 0 && (
            <div className="text-center py-12">
              <Trophy className="h-16 w-16 text-purple-400 mx-auto mb-4 opacity-50" />
              <p className="text-purple-200 text-lg">Complete your first project to start building your portfolio!</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
