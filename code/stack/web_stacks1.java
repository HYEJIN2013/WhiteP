> Gives more than one object an opportunity 
> to handle a request by linking receiving objects together.


//Handler
public interface EmailHandler
{
	//reference to the next handler in the chain
	public void setNext(EmailHandler handler);
		
	//handle request
	public void handleRequest(Email email);
}

public class BusinessMailHandler implements EmailHandler
{
	private EmailHandler next;

	public void setNext(EmailHandler handler)
	{
	    next = handler;
	}
	
	public void handleRequest(Email email)
    {
		if(!email.getFrom().endsWith("@businessaddress.com")
		{
		    next.handleRequest(email);
		}
		else
		{
		    //handle request (move to correct folder)
		}

	}	

}
