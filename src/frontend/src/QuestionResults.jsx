import { useState } from 'react';

export default function QuestionResults({ questionData, onBack, onVoteAgain }) {
  const [showDetails, setShowDetails] = useState(false);

  const getTotalVotes = () => {
    return questionData.choices.reduce((total, choice) => total + choice.votes, 0);
  };

  const getPercentage = (votes) => {
    const total = getTotalVotes();
    return total === 0 ? 0 : Math.round((votes / total) * 100);
  };

  const getUserChoice = () => {
    return questionData.choices.find(choice => choice.id === questionData.voted_choice_id);
  };

  const getCorrectChoice = () => {
    return questionData.choices.find(choice => choice.correct);
  };

  const userChoice = getUserChoice();
  const correctChoice = getCorrectChoice();
  const isCorrect = userChoice && userChoice.correct;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-800 to-slate-600 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button 
            onClick={onBack} 
            className="btn btn-ghost text-white hover:bg-white/10"
          >
            ← Back to Questions
          </button>
        </div>

        {/* Results Card */}
        <div className="card bg-white/95 backdrop-blur-lg shadow-2xl">
          <div className="card-body p-8">
            <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
              {questionData.question_text}
            </h1>

            {/* Result Status */}
            <div className="text-center mb-8">
              {isCorrect ? (
                <div className="alert alert-success">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span className="text-lg font-semibold">Correct! Well done! ✅</span>
                </div>
              ) : (
                <div className="alert alert-error">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                  <span className="text-lg font-semibold">Incorrect. Try again! ❌</span>
                </div>
              )}
            </div>

            {/* User's Choice */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Your Answer:</h3>
              <div className="p-4 bg-blue-50 border-l-4 border-blue-400 rounded">
                <p className="text-gray-800">{userChoice?.choice_text}</p>
              </div>
            </div>

            {/* Correct Answer (if user was wrong) */}
            {!isCorrect && correctChoice && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-700 mb-2">Correct Answer:</h3>
                <div className="p-4 bg-green-50 border-l-4 border-green-400 rounded">
                  <p className="text-gray-800">{correctChoice.choice_text}</p>
                </div>
              </div>
            )}

            {/* Show/Hide Detailed Results Button */}
            <div className="text-center mb-6">
              <button 
                onClick={() => setShowDetails(!showDetails)}
                className="btn btn-outline btn-sm"
              >
                {showDetails ? 'Hide' : 'Show'} Detailed Results
              </button>
            </div>

            {/* Detailed Results */}
            {showDetails && (
              <div className="space-y-4 mb-8">
                <h3 className="text-lg font-semibold text-gray-700 mb-4">
                  All Answers ({getTotalVotes()} total votes):
                </h3>
                
                {questionData.choices.map((choice) => {
                  const percentage = getPercentage(choice.votes);
                  const isUserChoice = choice.id === questionData.voted_choice_id;
                  
                  return (
                    <div key={choice.id} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className={`text-sm font-medium ${
                          choice.correct ? 'text-green-600' : 'text-gray-700'
                        }`}>
                          {choice.choice_text}
                          {choice.correct && ' ✅'}
                          {isUserChoice && ' (Your choice)'}
                        </span>
                        <span className="text-sm text-gray-500">
                          {choice.votes} votes ({percentage}%)
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all duration-500 ${
                            choice.correct 
                              ? 'bg-green-500' 
                              : isUserChoice 
                                ? 'bg-blue-500' 
                                : 'bg-gray-400'
                          }`}
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Action Buttons */}
            <div className="card-actions justify-center gap-4">
              <button 
                onClick={onVoteAgain} 
                className="btn btn-primary"
              >
                Vote Again
              </button>
              <button 
                onClick={onBack} 
                className="btn btn-outline"
              >
                Back to Questions
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
