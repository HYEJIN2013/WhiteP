var React = require('react');

var QuestionList = React.createClass({
  renderItems(question,index){
    return(
      <div key={index} className="col-xs-12 col-sm-6 col-md-3">
        <span>{question.text}</span>
      </div>
    );
  },
  render(){
    return(
      <div id="questions" clasName="row">
      <h2>Questions</h2>
        {this.props.questions.map(this.renderItems)}
      </div>
    );
  }
});


module.exports = React.createClass({
  getInitialState(){
  return { questions: [],
           text: ""
         }
  },
  onChange(e){
    this.setState({text:e.target.value});
  },
  handleSubmit(e){
    e.preventDefault();
    if(this.state.text){
      var nextQuestions = this.state.questions.concat([{
        text:this.state.text
      }]);
      this.setState({
        questions: nextQuestions,
        text: " "
      });
    }
  },
  render(){
    return (
        <div>
        <QuestionList questions={this.state.questions} />  
        <form className="fixed"onSubmit={this.handleSubmit}>
          <fieldset className="form-group">
            <label>Question</label>
            <input onChange={this.onChange}
                   value={this.state.text}
                   className="form-control"
                   id="question"
                   placeholder="Enter question.." />
          </fieldset>
        <button type="submit" className="btn btn-primary">Add</button>
        </form>
      </div>
    );
  }
});
