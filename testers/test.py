import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Book } from "@/entities/Book";
import { User } from "@/entities/User";
import { Sparkles, BookOpen, Coffee } from "lucide-react";
import BookSection from "../components/books/BookSection";

export default function Dashboard() {
  const [books, setBooks] = useState([]);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [booksData, userData] = await Promise.all([
        Book.list('-updated_date'),
        User.me().catch(() => ({ full_name: 'Reader' }))
      ]);
      setBooks(booksData);
      setUser(userData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const currentlyReading = books.filter(book => book.status === 'reading');
  const weeksPicks = books.filter(book => book.status === 'featured');

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-burgundy rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
            <BookOpen className="w-8 h-8 text-white" />
          </div>
          <p className="text-gray-600 text-lg">Loading your library...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 lg:p-12">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-12"
        >
          <div className="bg-gradient-to-r from-burgundy to-burgundy-dark rounded-3xl p-8 lg:p-12 text-white shadow-2xl">
            <div className="flex items-center gap-4 mb-6">
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
              >
                <Coffee className="w-8 h-8 text-gold" />
              </motion.div>
              <div>
                <h1 className="text-4xl lg:text-5xl font-bold mb-2">
                  {getGreeting()}, {user?.full_name || 'Reader'}!
                </h1>
                <p className="text-burgundy-light text-lg lg:text-xl">
                  Ready to dive into your next great adventure?
                </p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <BookOpen className="w-6 h-6 text-gold" />
                  <span className="font-semibold">Currently Reading</span>
                </div>
                <p className="text-2xl font-bold">{currentlyReading.length}</p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Sparkles className="w-6 h-6 text-gold" />
                  <span className="font-semibold">Books This Year</span>
                </div>
                <p className="text-2xl font-bold">{books.filter(b => b.status === 'completed').length}</p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Coffee className="w-6 h-6 text-gold" />
                  <span className="font-semibold">Total Books</span>
                </div>
                <p className="text-2xl font-bold">{books.length}</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Currently Reading Section */}
        <BookSection
          title="Currently Reading"
          subtitle="Continue your literary journey"
          books={currentlyReading}
          showProgress={true}
        />

        {/* This Week's Picks */}
        <BookSection
          title="This Week's Picks"
          subtitle="Curated recommendations just for you"
          books={weeksPicks}
          showProgress={false}
        />
      </div>
    </div>
  );
}

      {/* Footer */}
      <footer className="bg-gray-800 text-white text-center py-6 mt-12">
        <div className="container mx-auto">
          <p className="text-sm">&copy; 2023 Little Library. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}