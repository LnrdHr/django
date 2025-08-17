import { useState, useEffect} from 'react';
import axios from 'axios';
import './App.css'
import QuestionDetail from './QuestionDetail';
import QuestionResults from './QuestionResults';


export default function Index() {
  const [latestQuestionList, setLatestQuestionList] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [currentResponse, setCurrentResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Navigation state
  const [currentView, setCurrentView] = useState('list'); // 'list', 'detail', 'results'
  const [selectedQuestionId, setSelectedQuestionId] = useState(null);
  const [resultsData, setResultsData] = useState(null);

  const fetchLatestQuestions = async () => {
      try {
        const response = await axios.get('/api/questions/');
        setLatestQuestionList(response.data);
        console.log('Latest questions fetched:', response.data.length, 'questions');
      } catch (error) {
        console.error('Error fetching latest questions:', error);
      }
    };

    const sendUserMessage = async (message) => {
      try {
        setCurrentQuestion(message);
        setCurrentResponse('');
        setIsLoading(true);
        
        const response = await axios.post('/polls/send_user_message/', { message });
        setCurrentResponse(response.data.response || 'Response received');
        setIsLoading(false);
      } catch (error) {
        console.error('Error sending user message:', error);
        setCurrentResponse('Sorry, there was an error processing your question.');
        setIsLoading(false);
      }
    };

  // Navigation handlers
  const handleQuestionClick = (questionId) => {
    setSelectedQuestionId(questionId);
    setCurrentView('detail');
  };

  const handleVote = (voteResults) => {
    setResultsData(voteResults);
    setCurrentView('results');
  };

  const handleBackToList = () => {
    setCurrentView('list');
    setSelectedQuestionId(null);
    setResultsData(null);
  };

  const handleVoteAgain = () => {
    setCurrentView('detail');
    setResultsData(null);
  };

  useEffect(() => {
    fetchLatestQuestions();

  

    return () => {  
      setLatestQuestionList([]); // Cleanup function that resets the state once the call is completed
    };


  }, []);

  // Render different views based on current state
  if (currentView === 'detail' && selectedQuestionId) {
    return (
      <QuestionDetail 
        questionId={selectedQuestionId}
        onBack={handleBackToList}
        onVote={handleVote}
      />
    );
  }

  if (currentView === 'results' && resultsData) {
    return (
      <QuestionResults 
        questionData={resultsData}
        onBack={handleBackToList}
        onVoteAgain={handleVoteAgain}
      />
    );
  }

  // Default list view
  return (
    <div className="main-container">
      {/* Questions Section - Takes most of the screen */}
      <div className="questions-section">
        <h1 className="text-3xl font-bold text-center text-white">Choose a Question</h1>
        <div className="questions-container">
            {latestQuestionList && latestQuestionList.length > 0 ? (
              latestQuestionList.map((q) => (
                <div className="question-item" key={q.id}>
                  <div onClick={() => handleQuestionClick(q.id)}>
                    {q.question_text}
                  </div>
                </div>
              ))
            ) : (
              <div className="flex items-center justify-center col-span-full h-full">
                <div className="text-center">
                  <span className="loading loading-spinner loading-lg"></span>
                  <p className="mt-4 text-gray-600">Loading questions...</p>
                </div>
              </div>
            )}
        </div>
      </div>

      {/* Chat Section - DaisyUI Chat */}
      <div className="chat-container">
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto">
          {currentQuestion && (
            <div className="chat chat-end">
              <div className="chat-bubble chat-bubble-primary">
                {currentQuestion}
              </div>
            </div>
          )}
          
          {isLoading && (
            <div className="chat chat-start">
              <div className="chat-image avatar">
                <div className="w-10 rounded-full">
                  <span className="text-2xl">🤖</span>
                </div>
              </div>
              <div className="chat-bubble">
                <span className="loading loading-dots loading-sm"></span>
              </div>
            </div>
          )}
          
          {currentResponse && !isLoading && (
            <div className="chat chat-start">
              <div className="chat-image avatar">
                <div className="w-10 rounded-full">
                  <span className="text-2xl">🤖</span>
                </div>
              </div>
              <div className="chat-bubble">
                {currentResponse}
              </div>
            </div>
          )}
        </div>
        
        {/* Input Form */}
        <form 
          className="flex gap-3 items-center"
          onSubmit={(e) => {
            e.preventDefault();
            const message = e.target.message.value;
            if (message.trim()) {
              sendUserMessage(message);
              e.target.reset();
            }
          }}
        >
          <input 
            type="text" 
            name="message" 
            placeholder="Ask me anything..." 
            className="input input-bordered flex-1 bg-white/10 border-white/20 text-white placeholder-gray-300 focus:border-blue-400"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={isLoading}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}

